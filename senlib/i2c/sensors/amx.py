# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('AM2315')

import logging
logger = logging.getLogger('amx')
import time
from senlib.core.i2c import Sensor as I2CSensor


class AM2315(I2CSensor):

    DRIVER_NAME = 'am2315'

    ADDR = 0x5c
    DEFAULT_ADDR = ADDR

    FC_READ_REG = 0x03
    FC_WRITE_REG = 0x10

    HUM_H = 0x00
    HUM_L = 0x01
    TMP_H = 0x02
    TMP_L = 0x03

    MIN_SAMPLING_PERIOD = 2

    def __init__(self, i2c_ctrl, addr=DEFAULT_ADDR):
        super(AM2315, self).__init__(i2c_ctrl, addr)
        logger.debug('create AM2315(addr=%s) object', addr)
        self._temperature = self._humidity = 0.0
        self._wakeup()
        self._time = 0

    def _wakeup(self):
        logger.debug('call AM2315._wakeup()')
        try:
            self._i2c_ctrl.write_byte(self.addr, 0x00)
            logger.debug('AM2315 is awake')
        except OSError as e:
            logger.debug('AM2315 was not awake, but should be awake now')

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _read_data(self):
        _time = time.time()
        if self.MIN_SAMPLING_PERIOD > _time - self._time:
            logger.debug('ignore call AM2315._read_data(): sampling is below 2s')
            return

        self._time = _time
        logger.debug('call AM2315._read_data()')
        self._wakeup()

        try:
            self._i2c_ctrl.write_i2c_block_data(self.addr, self.FC_READ_REG, [0x00, 0x04])
            time.sleep(0.0015)
            vals = self._i2c_ctrl.read_i2c_block_data(self.addr, self.FC_READ_REG, 8)
            fn_code, nbytes, hum_msb, hum_lsb, temp_msb, temp_lsb, crc_lsb, crc_msb = vals

            hum = (hum_msb << 8) | hum_lsb
            temp = (temp_msb << 8) | temp_lsb
            crc_code =  (crc_msb << 8) | crc_lsb
            self._humidity = hum / 10.0
            self._temperature = temp / 10.0

            crc = self._compute_crc16(vals, 6)
            crc_check = crc == crc_code
            logger.debug('call AM2315._compute_crc16(data=%s, %s)=%s', vals, 6, crc)
            logger.debug('crc_code: %s, crc: %s, crc_check: %s', crc_code, crc,
                    crc_check)

        except OSError as e:
            logger.debug('AM2315 is probably not awake, OSError: %s', e)

    def _compute_crc16(self, data, length):
        crc = 0xffff
        for i in range(length):
            crc ^=  data[i]
            for j in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xa001
                else:
                    crc >>= 1
        return crc

    def read_temperature(self):
        self._read_data()
        return self._temperature

    def read_humidity(self):
        self._read_data()
        return self._humidity

    def measure(self):
        self._read_data()

        return {
            'temperature': self._temperature,
            'humidity': self._humidity
        }

    def temperature(self):
        return self._temperature

    def humidity(self):
        return self._humidity


class AM2321(AM2315):

    DRIVER_NAME = 'am2321'

    ADDR = 0x5c
    DEFAULT_ADDR = ADDR

    def __init__(self, i2c_ctrl, addr=DEFAULT_ADDR):
        super(AM2321, self).__init__(i2c_ctrl, addr)
        logger.debug('create AM2321(addr=%s) object', addr)


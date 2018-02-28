# -*- coding: utf-8 -*-
__author__ = 'Alexander Rüedlinger'
__all__ = ('MPL115A2')

from senlib import logger
import time
import struct
from senlib.core.i2c import Sensor as I2CSensor


class MPL115A2(I2CSensor):
    """
    This is a driver implementation for the Freescale MPL115A2 barometer sensor
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'mpl115a2'

    ADDR = 0x60
    DEFAULT_ADDR = ADDR

    REG_PADC = 0x00
    REG_TADC = 0x02
    CMD_CONVERT = 0x12

    REG_A0 = 0x04
    REG_B1 = 0x06
    REG_B2 = 0x08
    REG_C12 = 0x0A

    def __init__(self, bus, addr=DEFAULT_ADDR):
        super(MPL115A2, self).__init__(bus, addr)
        logger.debug('create MPL115A2(addr=%s) object', addr)
        self.dig_A0 = self.dig_B1 = self.dig_B2 = self.dig_C12 = 0.0

        self._pressure = self._temperature = 0.0
        self._calibration_data = {}
        self._read_calibration_data()

    @property
    def calibration_data(self):
        return self._calibration_data


    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _read_calibration_data(self):
        logger.debug('read calibration data')
        calib_data = self._bus.read_i2c_block_data(self.addr, self.REG_A0, 8)
        self.dig_A0, self.dig_B1, self.dig_B2, self.dig_C12 = struct.unpack('>hhhh', bytearray(calib_data))
        self.dig_A0 /= 8.0
        self.dig_B1 /= 8192.0
        self.dig_B2 /= 16384.0
        self.dig_C12 /= 16777216.0
        keys = ['A0', 'B1', 'B2', 'C12']
        values = [self.dig_A0, self.dig_B1, self.dig_B2, self.dig_C12]
        self._calibration_data = dict(zip(keys, values))
        for key, val in self._calibration_data.items():
            logger.debug('%s=%s', key, val)

    def _read_adc_t(self):
        msb, lsb = self._bus.read_i2c_block_data(self.addr, self.REG_TADC, 2)
        adc_t = ((msb << 8) | lsb) >> 6
        return adc_t

    def read_pressure(self):
        logger.debug('read pressure data')
        self._bus.write_byte_data(self.addr, self.CMD_CONVERT, 0x00)
        time.sleep(5/1000.0)

        adc_t = self._read_adc_t()
        msb, lsb = self._bus.read_i2c_block_data(self.addr, self.REG_PADC, 2)
        adc_p = ((msb << 8) | lsb) >> 6
        p_comp = self.dig_A0 + (self.dig_B1 + self.dig_C12 * adc_t) * adc_p + self.dig_B2 * adc_t
        return ((p_comp / 15.737) + 50.0) * 1000

    def read_temperature(self):
        # black magic temperature formula: http://forums.adafruit.com/viewtopic.php?f=25&t=34787
        # thx @park
        logger.debug('read temperature data')
        self._bus.write_byte_data(self.addr, self.CMD_CONVERT, 0x00)
        time.sleep(5/1000.0)

        adc_t = self._read_adc_t()
        t = adc_t * -0.1706 + 112.27
        return t

    def pressure(self):
        return self._pressure

    def temperature(self):
        return self._temperature

    def measure(self):
        self._pressure = self.read_pressure()
        self._temperature = self.read_temperature()

        return {
            'pressure': self._pressure,
            'temperature': self._temperature
        }


class MPL3115A2(I2CSensor):
    """
    This is a driver implementation for the MPL3115A2 sensor
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'mpl3115a2'

    ADDR = 0x60
    DEFAULT_ADDR = ADDR

    CTRL_REG1 = 0x26
    PT_DATA_CFG = 0x13

    MODE_BAROMETER = 0
    MODE_ALTIMETER = 1
    RAW = 0
    OS = 0x7
    RST = 0
    OST = 0
    SBYB = 1

    DREM = 1
    PDEFE = 1
    TDEFE = 1

    def __init__(self, bus, addr=DEFAULT_ADDR):
        super(MPL3115A2, self).__init__(bus, addr)
        logger.debug('create MPL3115A2(addr=%s) object', addr)
        self._mode = self.MODE_BAROMETER
        self._raw = self.RAW
        self._os = self.OS
        self._rst = self.RST
        self._ost = self.OST
        self._sbyb = self.SBYB

        settings = self._mode << 7
        settings |= (self._raw << 6)
        settings |= (self._os << 3)
        settings |= (self._rst << 2)
        settings |= (self._ost << 1)
        settings |= self._sbyb

        # enable data flags in PT_DATA_CFG
        pt_data_cfg = (self.DREM << 2)
        pt_data_cfg |= (self.PDEFE << 1)
        pt_data_cfg |= self.TDEFE
        self._bus.write_byte_data(self.addr, self.PT_DATA_CFG, pt_data_cfg)

        # set settings
        self._bus.write_byte_data(self.addr, self.CTRL_REG1, settings)

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _wait(self):
        while True: # busy waiting
            sta = self._bus.read_byte_data(self.addr, 0x00)
            if sta & 0x08: # check if data is ready
                break
            time.sleep(0.3)

    def _read_pressure_data(self, wait=False):
        logger.debug('read pressure data')
        if wait:
            self._wait()

        # the pressure value is representated as a Q18.2 fixed point
        p_msb = self._bus.read_byte_data(self.addr, 0x01)
        p_csb = self._bus.read_byte_data(self.addr, 0x02)
        p_lsb = self._bus.read_byte_data(self.addr, 0x03)
        p_data = (p_msb << 16 | (p_csb << 8) | p_lsb) >> 4
        return p_data / 4

    def _read_temperature_data(self, wait=False):
        logger.debug('read temperature data')
        if wait:
            self._wait()

        # the temperature value is representated as a Q8.4 fixed point
        t_msb = self._bus.read_byte_data(self.addr, 0x04)
        t_lsb = self._bus.read_byte_data(self.addr, 0x05)
        t_data = ((t_msb << 8) | t_lsb) >> 4
        return t_data / 16

    def read_pressure(self):
        return self._read_pressure_data(True)

    def read_temperature(self):
        return self._read_temperature_data(True)

    def pressure(self):
        return self._pressure

    def temperature(self):
        return self._temperature

    def measure(self):
        self._pressure = self._read_pressure_data(True)
        self._temperature = self._read_temperature_data(False)

        return {
            'pressure': self._pressure,
            'temperature': self._temperature
        }

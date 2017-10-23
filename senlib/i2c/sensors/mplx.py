# -*- coding: utf-8 -*-
__author__ = 'Alexander Rüedlinger'
__all__ = ('MPL115A2')

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

    def __init__(self, i2c_ctrl, addr=DEFAULT_ADDR):
        super(MPL115A2, self).__init__(i2c_ctrl, addr)
        self.dig_A0 = self.dig_B1 = self.dig_B2 = self.dig_C12 = 0.0

        self._pressure = self._temperature = 0.0

        self._read_coefficients()

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _read_coefficients(self):
        calib_data = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_A0, 8)
        self.dig_A0, self.dig_B1, self.dig_B2, self.dig_C12 = struct.unpack('>hhhh', bytearray(calib_data))
        self.dig_A0 /= 8.0
        self.dig_B1 /= 8192.0
        self.dig_B2 /= 16384.0
        self.dig_C12 /= 16777216.0

    def _read_adc_t(self):
        msb, lsb = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_TADC, 2)
        adc_t = ((msb << 8) | lsb) >> 6
        return adc_t

    def read_pressure(self):
        self._i2c_ctrl.write_byte_data(self.addr, self.CMD_CONVERT, 0x00)
        time.sleep(5/1000.0)

        adc_t = self._read_adc_t()
        msb, lsb = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_PADC, 2)
        adc_p = ((msb << 8) | lsb) >> 6
        p_comp = self.dig_A0 + (self.dig_B1 + self.dig_C12 * adc_t) * adc_p + self.dig_B2 * adc_t
        return ((p_comp / 15.737) + 50.0) * 1000

    def read_temperature(self):
        # black magic temperature formula: http://forums.adafruit.com/viewtopic.php?f=25&t=34787
        # thx @park
        self._i2c_ctrl.write_byte_data(self.addr, self.CMD_CONVERT, 0x00)
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
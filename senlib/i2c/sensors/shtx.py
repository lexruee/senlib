# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('SHT31')

import time
from senlib import logger
import struct
from senlib.core.i2c import Sensor as I2CSensor


class SHT31(I2CSensor):
    """
    This is a quick and dirty driver implementation for the sensor STH31 
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'sht31'

    ADDR1 = 0x44
    ADDR2 = 0x45
    DEFAULT_ADDR = ADDR1

    CS_ENABLED = 0x2C # clock stretching enabled
    CS_DISBALED = 0x24 # clock stretching disabled
    REP_HIGH_CS = 0x06
    REP_MEDIUM_CS = 0x0D
    REP_LOW_CS = 0x10
    REP_HIGH = 0x00
    REP_MEDIUM = 0x0B
    REP_LOW = 0x16
    REP_HIGH_S = 0.015

    CMD_SOFT_RESET = 0x30, 0xA2

    def __init__(self, bus, addr=DEFAULT_ADDR):
        super(SHT31, self).__init__(bus, addr)
        logger.debug('create SHT31(addr=%s) object', addr)
        self._temperature = self._humidity = 0.0
        self._repeatability = self.REP_HIGH
        self._soft_reset()

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _soft_reset(self):
        logger.debug('perform a soft reset')
        msb, lsb = self.CMD_SOFT_RESET
        self._bus.write_byte_data(self.addr, msb, lsb)

    def _trigger_measurement(self):
        logger.debug('trigger single shot measurement')
        self._bus.write_byte_data(self.addr, self.CS_DISBALED,
                self._repeatability)
 
    def _read_data(self):
        self._trigger_measurement()
        time.sleep(self.REP_HIGH_S)
        logger.debug('read temperature and humidity data')
        data = self._bus.read_i2c_block_data(self.addr, 0x00, 6)

        t_msb, t_lsb, t_crc, h_msb, h_lsb, h_crc = data
        t_word = (t_msb << 8) | t_lsb
        h_word = (h_msb << 8) | h_lsb

        self._temperature = self._compute_temperature_c(t_word) 
        self._humidity = self._compute_humidity(h_word)
        return self._temperature, self._humidity

    def _compute_temperature_c(self, t_raw):
        return -45 + (175 * t_raw)/65535.0

    def _compute_temperature_f(self, t_raw):
        return -49 + (315 * t_raw)/65535.0

    def _compute_humidity(self, h_raw):
        return 100 * (h_raw/65535.0)

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

    def pressure(self):
        return self._pressure

    def humidity(self):
        return self._humidity

# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('STH31')

import logging
logger = logging.getLogger('bmex')
import struct
from senlib.core.i2c import Sensor as I2CSensor


class SHT31(I2CSensor):
    """
    This is a quick and dirty driver implementation for the sensor STH31 
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'sht31'

    ADDR = 0x44
    DEFAULT_ADDR = ADDR

    def __init__(self, bus, addr=DEFAULT_ADDR):
        super(SHT31, self).__init__(bus, addr)
        logger.debug('create SHT31(addr=%s) object', addr)
        self._temperature = self._humidity = 0.0
        
    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def read_temperature(self):
        pass

    def read_humidity(self):
        pass

    def measure(self):
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

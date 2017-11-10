# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('LM75')

import logging
logger = logging.getLogger('lmx')
from senlib.core.i2c import Sensor as I2CSensor


class LM75(I2CSensor):
    """
    This is a software driver implementation for the Maxim LM75 temperature sensor
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'lm75'

    ADDR = 0x48
    DEFAULT_ADDR = ADDR

    REG_TMP = 0x00
    REG_CONF = 0x01
    REG_THYST = 0x02
    REG_TOS = 0x03

    def __init__(self, bus, addr=ADDR):
        super(LM75, self).__init__(bus, addr)
        logger.debug('create LM75(addr=%s) object', addr)
        self._temperature = 0.0

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def read_temperature(self):
        logger.debug('read temperature data')
        data = self._bus.read_word_data(self.addr, self.REG_TMP)
        msb = data & 0x00ff
        lsb = (data & 0xff00) >> 8
        t0 = msb
        t1 = (lsb & 0x80) >> 7 
        temperature = t0 + 0.5 * t1 
        return temperature

    def measure(self):
        self._temperature = self.read_temperature()

        return {
            'temperature': self._temperature
        }

    def temperature(self):
        return self._temperature

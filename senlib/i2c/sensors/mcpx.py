# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('MCP9808')

import logging
logger = logging.getLogger('mcpx')
from senlib.core.i2c import Sensor as I2CSensor


class MCP9808(I2CSensor):
    """
    This is a software driver implementation for the Microchip MCP9808 
    temperature sensor for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'mcp9808'

    ADDR = 0x18
    DEFAULT_ADDR = ADDR

    REG_CONFIG = 0x01

    REG_ALERT = 0x04
    REG_TMP = 0x05
    REG_DEVICE_ID = 0x07
    REG_RES = 0x08

    def __init__(self, bus, addr=DEFAULT_ADDR):
        super(MCP9808, self).__init__(bus, addr)
        logger.debug('create MCP9808(addr=%s) object', addr)
        self.id = self._read_device_id()
        self._temperature = 0.0

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _read_device_id(self):
        logger.debug('read device id')
        return self._bus.read_byte_data(self.addr, self.REG_DEVICE_ID)

    def read_temperature(self):
        logger.debug('read temperature data')
        data = self._bus.read_word_data(self.addr, self.REG_TMP)
        msb = data & 0x00FF
        lsb = (data & 0xFF00) >> 8
        word = (msb << 8) | lsb
        temperature = word & 0x0FFF
        temperature /= 16.0

        if word & 0x1000:
            temperature -= 256
        return temperature

    def temperature(self):
        return self._temperature

    def measure(self):
        self._temperature = self.read_temperature()

        return {
            'temperature': self._temperature
        }

# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('BH1750FVI')

import time
from senlib import logger
import struct
from senlib.core.i2c import Sensor as I2CSensor


class BH1750(I2CSensor):
    """
    This is a quick and dirty driver implementation for the sensor BH1750FVI 
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'bh1750'

    ADDR_H = 0x5C
    ADDR_L = 0x23
    ADDR1 = ADDR_L
    ADDR2 = ADDR_H
    DEFAULT_ADDR = ADDR_L

    CMD_PWR_DOWN = 0x00
    CMD_PWR_ON = 0x01
    CMD_RST = 0x07

    CMD_HRES_MEAS_C = 0x10
    CMD_HRES2_MEAS_C = 0x11
    CMD_LRES_MEAS_C = 0x13

    CMD_HRES_MEAS = 0x20
    CMD_HRES2_MEAS = 0x21
    CMD_LRES_MEAS = 0x23

    MAX_TIME_HRES = 0.18
    MAX_TIME_HRES2 = 0.18
    MAX_TIME_LRES = 0.024
    
    MODE_HRES = 0
    MODE_HRES2 = 1
    MODE_LRES = 2

    MODE_HRES_C = 3
    MODE_HRES2_C = 4
    MODE_LRES_C = 5
    
    _MODES = {
            MODE_HRES: [CMD_HRES_MEAS, MAX_TIME_HRES],
            MODE_HRES2: [CMD_HRES2_MEAS, MAX_TIME_HRES2],
            MODE_LRES: [CMD_LRES_MEAS, MAX_TIME_LRES],
            MODE_HRES_C: [CMD_HRES_MEAS_C, MAX_TIME_HRES],
            MODE_HRES2_C: [CMD_HRES2_MEAS_C, MAX_TIME_HRES2],
            MODE_LRES_C: [CMD_LRES_MEAS_C, MAX_TIME_LRES]
     }

    def __init__(self, bus, addr=DEFAULT_ADDR):
        super(BH1750, self).__init__(bus, addr)
        logger.debug('create %s(addr=%#04x) object', self.__class__.__name__, addr)
        self._illuminance = 0.0
        self._power_on()
        self._mode = None
        self._mode_data = None
        self._set_mode(self.MODE_HRES)
        self._reset()

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _set_mode(self, mode):
        self._mode = mode if mode in self._MODES else self.MODE_HRES
        self._mode_data = self._MODES[self._mode]
        cmd, _time = self._mode_data
        logger.debug('set mode to %s, measurement cmd: %#04x, max measurement time: %ss', 
                self._mode, cmd, _time)

    def _power_down(self):
        logger.debug('set state to power down')
        self._bus.write_byte(self.addr, self.CMD_PWR_DOWN)

    def _power_on(self):
        logger.debug('set state to power on')
        self._bus.write_byte(self.addr, self.CMD_PWR_ON)

    def _reset(self):
        logger.debug('perform a reset')
        self._bus.write_byte(self.addr, self.CMD_RST)

    def _trigger_measurement(self):
        logger.debug('trigger measurement')
        cmd, _ = self._mode_data
        self._bus.write_byte(self.addr, self.CMD_HRES_MEAS) 
 
    def _read_illuminance_data(self):
        self._trigger_measurement()
        _, _time = self._mode_data
        wait_s = 2 * _time
        logger.debug('wait %ss before reading measurement data', wait_s)
        time.sleep(wait_s)
        logger.debug('read measurement data')
        msb, lsb = self._bus.read_i2c_block_data(self.addr, 0x00, 2)
        i_word = (msb << 8) | lsb
        self._illuminance = i_word / 1.2
        return self._illuminance

    def read_illuminance(self):
       self._read_illuminance_data()
       return self._illuminance

    def measure(self):
        self._read_illuminance_data()
        return {
            'illuminance': self._illuminance
        }

    def illuminance(self):
        return self._illuminance

# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('HDC1008')

import time
from senlib.core.i2c import Sensor as I2CSensor


class HDC1008(I2CSensor):
    """
    This is a software driver implementation for the HDC1008 sensor
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'hdc1008'

    ADDR = 0x40
    DEFAULT_ADDR = ADDR
    
    REG_TMP = 0x00
    REG_HUM = 0x01
    REG_CONFIG = 0x02
    REG_ID_MSB = 0xFB
    REG_ID_CSB = 0xFC
    REG_ID_LSB = 0xFD

    RST = 0
    HEAT = 1
    MODE = 1 # humidity and temperature
    BTST = 0
    TRES = 0 # 14 bit resolution
    HRES = 0 # 14 bit resolution

    def __init__(self, i2c_ctrl, addr=DEFAULT_ADDR):
        super(HDC1008, self).__init__(i2c_ctrl, addr)
        self._temperature = self._humidity = 0.0
        settings = 0
        settings |= (self.RST << 15)
        settings |= (self.HEAT << 13)
        settings |= (self.MODE << 12)
        settings |= (self.BTST << 11)
        settings |= (self.TRES << 10)
        settings |= (self.HRES << 8)
        self._i2c_ctrl.write_word_data(self.addr, self.REG_CONFIG, settings)

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _trigger_temperature_measurement(self):
        self._i2c_ctrl.write_byte(self.addr, self.REG_TMP)
        time.sleep(0.015)

    def _trigger_humidity_measurement(self):
        self._i2c_ctrl.write_byte(self.addr, self.REG_HUM)
        time.sleep(0.015)

    def read_temperature(self):
        self._trigger_temperature_measurement()
        msb = self._i2c_ctrl.read_byte(self.addr)
        lsb = self._i2c_ctrl.read_byte(self.addr)
        tdata = (msb << 8) | lsb
        temp = (tdata / 65536.0) * 165 - 40
        return temp

    def temperature(self):
        return self._temperature

    def read_humidity(self):
        self._trigger_humidity_measurement()
        msb = self._i2c_ctrl.read_byte(self.addr)
        lsb = self._i2c_ctrl.read_byte(self.addr)
        hdata = (msb << 8) | lsb
        hum = (hdata / 65536.0) * 100
        return hum

    def humidity(self):
        return self._humidity

    def measure(self):
        self._temperature = self.read_temperature()
        self._humidity = self.read_humidity()

        return {
            'temperature': self._temperature,
            'humidity': self._humidity
        }


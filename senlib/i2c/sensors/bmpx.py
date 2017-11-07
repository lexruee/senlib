# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('BMP085', 'BMP180', 'BMP280')

import logging
logger = logging.getLogger('bmex')
import time
import struct
from senlib.core.i2c import Sensor as I2CSensor


class BMP085(I2CSensor):
    """
    This is a quick and dirty driver implementation for the Bosch BMP085 barometer sensor
    for use with Raspberry Pi computers.

    Remarks and credits:
        * The compensation functions for computing the temperature, pressure, and humidity values
          are based on the Adafruit Python BMP driver: https://github.com/adafruit/Adafruit_Python_BMP

    """

    DRIVER_NAME = 'bmp085'

    ADDR = 0x77
    DEFAULT_ADDR = ADDR

    REG_AC1 = 0xAA

    MODE_LOW = 0
    MODE_STANDARD = 1
    MODE_HIGH = 2
    MODE_ULTRA_HIGH = 3

    CTRL_READ_TEMP = 0x2E
    CTRL_READ_PRESS = 0x34

    REG_OUT_XLSB = 0xF8  # adc out: bits 7-3
    REG_OUT_LSB = 0xF7  # adc out: bits 7-0
    REG_OUT_MSB = 0xF6  # adc out: bits 7-0

    REG_CTRL_MEAS = 0xF4
    REG_SOF = 0xE0  # reset
    REG_ID = 0xD0

    def __init__(self, i2c_ctrl, addr=DEFAULT_ADDR):
        super(BMP085, self).__init__(i2c_ctrl, addr)
        logger.debug('create %s(addr=%s) object', self.DRIVER_NAME.upper(), addr)
        self.dig_AC1 = self.dig_AC2 = self.dig_AC3 = self.dig_AC4 = self.dig_AC5 = self.dig_AC6 = self.dig_B1 = \
            self.dig_B2 = self.dig_MB = self.dig_MC = self.dig_MD = 0

        self.mode = self.MODE_STANDARD
        self.id = self._read_id()

        self._temperature = self._pressure = 0

        self._read_calibration_data()

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _read_id(self):
        logger.debug('read device id')
        return self._i2c_ctrl.read_byte_data(self.addr, self.REG_ID)

    def _compensate_temperature(self, UT):
        X1 = ((UT - self.dig_AC6) * self.dig_AC5) >> 15
        X2 = (self.dig_MC << 11) // (X1 + self.dig_MD)
        B5 = X1 + X2
        temp = ((B5 + 8) >> 4) / 10.0
        return temp

    def _compensate_pressure(self, UT, UP):
        X1 = ((UT - self.dig_AC6) * self.dig_AC5) >> 15
        X2 = (self.dig_MC << 11) // (X1 + self.dig_MD)
        B5 = X1 + X2

        B6 = B5 - 4000
        X1 = (self.dig_B2 * (B6 * B6) >> 12) >> 11
        X2 = (self.dig_AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.dig_AC1 * 4 + X3) << self.mode) + 2) // 4
        X1 = (self.dig_AC3 * B6) >> 13
        X2 = (self.dig_B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.dig_AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self.mode)

        if B7 < 0x80000000:
            p = (B7 * 2) // B4
        else:
            p = (B7 // B4) * 2

        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        pressure = p + ((X1 + X2 + 3791) >> 4)
        return pressure

    def read_temperature(self):
        temp, _ = self._read_sensor_data()
        return temp

    def read_pressure(self):
        _, pressure = self._read_sensor_data()
        return pressure

    def _read_sensor_data(self):
        adc_t, adc_p = self._read_raw_temperature(), self._read_raw_pressure()
        return self._compensate_temperature(adc_t), self._compensate_pressure(adc_t, adc_p)

    def _read_raw_temperature(self):
        logger.debug('read temperature data')
        self._i2c_ctrl.write_byte_data(self.addr, self.REG_CTRL_MEAS, self.CTRL_READ_TEMP)
        time.sleep(0.005)
        msb, lsb = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_OUT_MSB, 2)
        adc_t = (msb << 8) | lsb
        return adc_t

    def _read_raw_pressure(self):
        logger.debug('read pressure data')
        self._i2c_ctrl.write_byte_data(self.addr, self.REG_CTRL_MEAS, self.CTRL_READ_PRESS + (self.mode << 6))

        if self.mode == self.MODE_LOW:
            time.sleep(0.005)
        elif self.mode == self.MODE_HIGH:
            time.sleep(0.014)
        elif self.mode == self.MODE_ULTRA_HIGH:
            time.sleep(0.026)
        else:
            time.sleep(0.008)

        msb, lsb, xlsb = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_OUT_MSB, 3)
        adc_p = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.mode)
        return adc_p

    def _read_calibration_data(self):
        logger.debug('read calibration data')
        dig_AC1_MD = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_AC1, 22)
        dig_AC1_MD = struct.unpack('>hhhHHHhhhhh',  bytearray(dig_AC1_MD))
        self.dig_AC1, self.dig_AC2, self.dig_AC3, self.dig_AC4, self.dig_AC5, self.dig_AC6, self.dig_B1, self.dig_B2, \
            self.dig_MB, self.dig_MC, self.dig_MD = dig_AC1_MD
        logger.debug('AC1=%s, AC2=%s, AC3=%s, AC4=%s, AC5=%s, AC6=%s', self.dig_AC1, 
                self.dig_AC2, self.dig_AC3, self.dig_AC4, self.dig_AC5, self.dig_AC6)
        logger.debug('B1=%s, B2=%s, B=%s, MC=%s, MD=%s', self.dig_B1, self.dig_B2, 
                self.dig_MB, self.dig_MC, self.dig_MD)

    def measure(self):
        self._temperature, self._pressure = self._read_sensor_data()

        return {
            'temperature': self._temperature,
            'pressure': self._pressure
        }

    def temperature(self):
        return self._temperature

    def pressure(self):
        return self._pressure


class BMP180(BMP085):

    DRIVER_NAME = 'bmp180'

    def __init__(self, i2c_ctrl, addr=BMP085.DEFAULT_ADDR):
        super(BMP180, self).__init__(i2c_ctrl, addr)


class BMP280(I2CSensor):
    """
    This is a quick and dirty driver implementation for the Bosch BMP280 barometer sensor
    for use with Raspberry Pi computers.
    """

    DRIVER_NAME = 'bmp280'

    ADDR1 = 0x76
    ADDR2 = 0x77
    DEFAULT_ADDR = ADDR2

    REG_TEMP = 0xFA
    REG_PRESS = 0xF7

    REG_CONFIG = 0xF5
    REG_CTRL_MEAS = 0xF4

    def __init__(self, i2c_ctrl, addr=DEFAULT_ADDR):
        super(BMP280, self).__init__(i2c_ctrl, addr)
        logger.debug('create BMP280(addr=%s) object', addr)
        self.dig_T1 = self.dig_T2 = self.dig_T3 = 0
        self.dig_P1 = self.dig_P2 = self.dig_P3 = self.dig_P4 = self.dig_P5 = self.dig_P6 = self.dig_P7 \
            = self.dig_P8 = self.dig_P9 = 0

        self.t_fine = 0.0
        self._temperature = self._humidity = self._pressure = 0.0

        self._read_calibration_data()

        self.osrs_h = 1
        self.osrs_t = 1
        self.osrs_p = 1
        self.power_mode = 3
        self.filter = 0
        self.t_sb = 5

        self._set_settings()
        self._set_config()

    @classmethod
    def driver_name(cls):
        return cls.DRIVER_NAME

    @classmethod
    def default_addr(cls):
        return cls.DEFAULT_ADDR

    def _set_meas(self):
        logger.debug('configure temperature and pressure osrs')
        settings = 0
        settings |= (self.osrs_t << 5)
        settings |= (self.osrs_p << 2)
        settings |= self.power_mode
        self._i2c_ctrl.write_byte_data(self.addr, self.REG_CTRL_MEAS, settings)

    def _set_settings(self):
        self._set_meas()

    def _set_config(self):
        logger.debug('configure sensor')
        config = 0
        config |= (self.t_sb << 5)
        config |= (self.filter << 2)
        self._i2c_ctrl.write_byte_data(self.addr, self.REG_CONFIG, config)

    def _read_calibration_data(self):
        logger.debug('read calibration data')
        dig_88_A1 = self._i2c_ctrl.read_i2c_block_data(self.addr, 0x88, 26)
        dig_88_A1 = struct.unpack('<HhhHhhhhhhhhBB', bytearray(dig_88_A1))
        self.dig_T1, self.dig_T2, self.dig_T3, self.dig_P1, self.dig_P2, self.dig_P3, self.dig_P4, self.dig_P5, \
        self.dig_P6, self.dig_P7, self.dig_P8, self.dig_P9, _, self.dig_H1 = dig_88_A1

        logger.debug('T1=%s, T2=%s, T3=%s', self.dig_T1, self.dig_T2,
                self.dig_T3)
        logger.debug('P1=%s, P2=%s, P3=%s, P4=%s, P5=%s, P6=%s, P7=%s, P8=%s, P9=%s', 
                self.dig_P1, self.dig_P2, self.dig_P3, self.dig_P4, self.dig_P5, 
                self.dig_P6, self.dig_P7, self.dig_P8, self.dig_P9)
        logger.debug('H1=%s', self.dig_H1)
 
    def _read_raw_sensor_data(self):
        logger.debug('read pressure data')
        press_msb, press_lsb, press_xlsb = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_PRESS, 3)
        logger.debug('read temperature data')
        temp_msb, temp_lsb, temp_xlsb = self._i2c_ctrl.read_i2c_block_data(self.addr, self.REG_TEMP, 3)

        adc_p = (press_msb << 12) | (press_lsb << 4) | (press_xlsb >> 4)
        adc_t = (temp_msb << 12) | (temp_lsb << 4) | (temp_xlsb >> 4)

        return adc_p, adc_t

    def _compensate_temperature(self, adc_t):
        UT = float(adc_t)
        var1 = (UT / 16384.0 - self.dig_T1 / 1024.0) * float(self.dig_T2)
        var2 = ((UT / 131072.0 - self.dig_T1 / 8192.0) * (
        UT / 131072.0 - self.dig_T1 / 8192.0)) * float(self.dig_T3)
        self.t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        return temp

    def _compensate_pressure(self, adc_p):
        var1 = self.t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self.dig_P6 / 32768.0
        var2 = var2 + var1 * self.dig_P5 * 2.0
        var2 = var2 / 4.0 + self.dig_P4 * 65536.0
        var1 = (
               self.dig_P3 * var1 * var1 / 524288.0 + self.dig_P2 * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self.dig_P1
        if var1 == 0:
            return 0
        p = 1048576.0 - adc_p
        p = ((p - var2 / 4096.0) * 6250.0) / var1
        var1 = self.dig_P9 * p * p / 2147483648.0
        var2 = p * self.dig_P8 / 32768.0
        p = p + (var1 + var2 + self.dig_P7) / 16.0
        return p

    def read_temperature(self):
        adc_p, adc_t = self._read_raw_sensor_data()
        return self._compensate_temperature(adc_t)

    def read_pressure(self):
        adc_p, adc_t = self._read_raw_sensor_data()
        self._compensate_temperature(adc_t)
        return self._compensate_pressure(adc_p)

    def measure(self):
        adc_p, adc_t = self._read_raw_sensor_data()
        self._temperature = self._compensate_temperature(adc_t)
        self._pressure = self._compensate_pressure(adc_p)

        return {
            'temperature': self._temperature,
            'pressure': self._pressure
        }

    def temperature(self):
        return self._temperature

    def pressure(self):
        return self._pressure

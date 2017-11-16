# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ()

from .sensors import amx
from .sensors import bhx
from .sensors import bmex
from .sensors import bmpx
from .sensors import hdcx
from .sensors import lmx
from .sensors import mcpx
from .sensors import mplx
from .sensors import shtx
from .sensors import six
from ..core.i2c import SMBus

_SENSORS = {
        'am2315': amx.AM2315,
        'am2321': amx.AM2321,
        'bh1750': bhx.BH1750,
        'bme280': bmex.BME280,
        'bmp085': bmpx.BMP085,
        'bmp180': bmpx.BMP180,
        'bmp280': bmpx.BMP280,
        'hdc1008': hdcx.HDC1008,
        'lm75': lmx.LM75,
        'mcp9808': mcpx.MCP9808,
        'mpl115a2': mplx.MPL115A2,
        'mpl3115a2': mplx.MPL3115A2,
        'sht31': shtx.SHT31,
        'si7021': six.SI7021
}

class DriverNotFound(Exception):
    pass


def get_sensor_driver(name):
    if name.lower() in _SENSORS:
        driver_class = _SENSORS[name]
        return driver_class
    else:
       raise DriverNotFound("Driver {} not found!".format(name))

def get_sensor(name, bus, addr):
    driver_class = get_sensor_driver(name)
    i2c_ctrl = SMBus(bus or 1)
    sensor = driver_class(i2c_ctrl, addr or driver_class.DEFAULT_ADDR)
    return sensor


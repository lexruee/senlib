# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ()

from .sensors import bmex
from .sensors import bmpx
from .sensors import lmx
from .sensors import mcpx
from .sensors import mplx
from .sensors import six
from ..core.i2c import Controller

_SENSORS = {
        'bme280': bmex.BME280,
        'bmp085': bmpx.BMP085,
        'bmp180': bmpx.BMP180,
        'bmp280': bmpx.BMP280,
        'lm75': lmx.LM75,
        'mcp9808': mcpx.MCP9808,
        'mpl115a2': mplx.MPL115A2,
        'si7021': six.SI7021
}

class DriverNotFound(Exception):
    pass


def get_sensor(name, bus, addr):
    if name.lower() in _SENSORS:
        driver_class = _SENSORS[name]
        i2c_ctrl = Controller(bus or 1)
        sensor = driver_class(i2c_ctrl, addr or driver_class.DEFAULT_ADDR)
        return sensor
    else:
       raise DriverNotFound("Driver {} not found!".format(name))


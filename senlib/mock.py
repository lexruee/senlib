# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('Sensor')


class Sensor(object):
    
    DRIVER_NAME = 'mock-sensor'

    def measure(self):
        return {
            'temperature': 29.5,
            'humidity': 35.2
        }

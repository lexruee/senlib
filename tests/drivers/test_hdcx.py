# -*- coding: utf-8 -*-
from senlib.i2c.sensors.hdcx import HDC1008
from senlib.core.i2c import MockBus

I2C_DATA_IN = [
    95, 95, 145, 145,
    96, 96, 149, 149,
    96, 96, 161, 161
]


def test_create_hdc1008():
    bus = MockBus(read_data=I2C_DATA_IN)
    sensor = HDC1008(bus=bus)
    assert sensor
    return sensor

def test_measure_hdc1008():
    sensor = test_create_hdc1008()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 21.47 <= 0.1
    assert sensor_data['humidity'] - 56.86 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 22.12 <= 0.1
    assert sensor_data['humidity'] - 58.43 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 22.12 <= 0.1
    assert sensor_data['humidity'] - 63.17 <= 0.1

def test_close_hdc1008():
    sensor = test_create_hdc1008()
    sensor_data = sensor.measure()
    sensor.close() 

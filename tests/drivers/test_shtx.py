# -*- coding: utf-8 -*-
from senlib.i2c.sensors.shtx import SHT31
from senlib.core.i2c import MockBus

I2C_DATA_IN = [
    [98, 60, 181, 109, 223, 190],
    [98, 44, 246, 110, 48, 124],
    [98, 50, 170, 110, 68, 64]
]


def test_create_sht31():
    bus = MockBus(read_data=I2C_DATA_IN)
    sensor = SHT31(bus=bus)
    assert sensor
    return sensor

def test_measure_sht31():
    sensor = test_create_sht31()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 22.15 <= 0.1
    assert sensor_data['humidity'] - 42.92 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 22.11 <= 0.1
    assert sensor_data['humidity'] - 43.04 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 22.12 <= 0.1
    assert sensor_data['humidity'] - 43.07 <= 0.1

def test_close_sht31():
    sensor = test_create_sht31()
    sensor_data = sensor.measure()
    sensor.close() 

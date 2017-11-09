# -*- coding: utf-8 -*-
from senlib.i2c.sensors.amx import AM2315
from senlib.i2c.sensors.amx import AM2321
from senlib.core.i2c import MockBus

AM2315.MIN_SAMPLING_PERIOD = 0
AM2321.MIN_SAMPLING_PERIOD = 0
I2C_DATA_IN = [
        [3, 4, 1, 241, 0, 203, 224, 112],
        [3, 4, 1, 242, 0, 203, 16, 112],
        [3, 4, 1, 243, 0, 203, 65, 176]
]


def test_create_am2315():
    bus = MockBus(read_data=I2C_DATA_IN)
    sensor = AM2315(bus=bus)
    assert sensor
    return sensor

def test_measure_am2315():
    sensor = test_create_am2315()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.3
    assert sensor_data['humidity'] == 49.7

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.3
    assert sensor_data['humidity'] == 49.8

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.3
    assert sensor_data['humidity'] == 49.9

def test_create_am2321():
    bus = MockBus(read_data=I2C_DATA_IN)
    sensor = AM2321(bus=bus)
    assert sensor
    return sensor

def test_measure_am2321():
    sensor = test_create_am2321()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.3
    assert sensor_data['humidity'] == 49.7

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.3
    assert sensor_data['humidity'] == 49.8

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.3
    assert sensor_data['humidity'] == 49.9


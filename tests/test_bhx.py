# -*- coding: utf-8 -*-
from senlib.i2c.sensors.bhx import BH1750
from senlib.core.i2c import MockBus

I2C_DATA_IN = [
    [0, 9],
    [0, 18],
    [0, 44],
    [7, 211]
]

def test_create_bh1750():
    bus = MockBus(read_data=I2C_DATA_IN)
    sensor = BH1750(bus=bus)
    assert sensor
    return sensor

def test_measure_bh1750():
    sensor = test_create_bh1750()
    sensor._mode_data = [0,0]

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['illuminance'] - 7.5 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['illuminance'] - 15.0 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['illuminance'] - 36.67 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['illuminance'] - 1669.167 <= 0.1

# -*- coding: utf-8 -*-
from senlib.i2c.sensors.six import SI7021
from senlib.core.i2c import MockBus


SI7021_I2C_DATA_IN = [
    124,
    124,
    97,
    97,
    157,
    157,
    98,
    98,
    146,
    146,
    97,
    97
]

def test_create_si7021():
    bus = MockBus(read_data=SI7021_I2C_DATA_IN)
    sensor = SI7021(bus=bus)
    assert sensor
    return sensor

def test_measure_si7021():
    sensor = test_create_si7021()
    
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['humidity'] - 54.78 <= 0.1
    assert sensor_data['temperature'] - 19.99 <= 0.1
    
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['humidity'] - 70.96 <= 0.1
    assert sensor_data['temperature'] - 20.68 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['humidity'] - 65.57 <= 0.1
    assert sensor_data['temperature'] - 19.99 <= 0.1

def test_close_si7021():
    sensor = test_create_si7021()
    sensor_data = sensor.measure()
    sensor.close() 

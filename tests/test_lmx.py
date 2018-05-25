# -*- coding: utf-8 -*-
from senlib.i2c.sensors.lmx import LM75
from senlib.core.i2c import MockBus


LM75_I2C_DATA_IN = [
    57362,
    49171,
    22,
    32789
]

def test_create_lm75():
    bus = MockBus(read_data=LM75_I2C_DATA_IN)
    sensor = LM75(bus=bus)
    assert sensor
    return sensor

def test_measure_lm75():
    sensor = test_create_lm75()
    
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 18.5
    
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 19.5

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 22.0

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 21.5

def test_close_lm75():
    sensor = test_create_lm75()
    sensor_data = sensor.measure()
    sensor.close() 

# -*- coding: utf-8 -*-
from senlib.i2c.sensors.mplx import MPL115A2
from senlib.i2c.sensors.mplx import MPL3115A2
from senlib.core.i2c import MockBus


MPL3115A2_I2C_DATA_IN = [238, 91, 25, 192, 20, 48] \
    + [238, 91, 25, 224, 20, 32] \
    + [238, 91, 32, 144, 19, 0]

def test_create_mpl3115a2():
    bus = MockBus(read_data=MPL3115A2_I2C_DATA_IN)
    sensor = MPL3115A2(bus=bus)
    assert sensor
    return sensor

def test_measure_mpl3115a2():
    sensor = test_create_mpl3115a2()
    
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.1875
    assert sensor_data['pressure'] == 93287.0

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.125
    assert sensor_data['pressure'] == 93287.5

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 19.0
    assert sensor_data['pressure'] == 93314.25

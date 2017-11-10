# -*- coding: utf-8 -*-
from senlib.i2c.sensors.mplx import MPL115A2
from senlib.i2c.sensors.mplx import MPL3115A2
from senlib.core.i2c import MockBus


MPL3115A2_I2C_DATA_IN = [238, 91, 25, 192, 20, 48] \
    + [238, 91, 25, 224, 20, 32] \
    + [238, 91, 32, 144, 19, 0]
MPL115A2_I2C_DATA_IN = [[60, 149, 182, 174, 198, 209, 50, 8]] \
    + [
        [130, 64],
        [104, 64],
        [130, 64],
        [133, 64],
        [103, 192],
        [132, 192],
        [132, 192],
        [103, 192],
        [133, 64]
]

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

def test_create_mpl115a2():
    bus = MockBus(read_data=MPL115A2_I2C_DATA_IN)
    sensor = MPL115A2(bus=bus)
    assert sensor
    return sensor

def test_measure_mpl115a2():
    sensor = test_create_mpl115a2()
    
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 23.39 <= 0.1
    assert sensor_data['pressure'] - 93433.76 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 21.68 <= 0.1
    assert sensor_data['pressure'] - 93234.67 <= 0.1

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 21.34 <= 0.1
    assert sensor_data['pressure'] - 93307.95 <= 0.1

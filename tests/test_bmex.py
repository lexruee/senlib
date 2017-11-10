# -*- coding: utf-8 -*-
from senlib.i2c.sensors.bmex import BME280
from senlib.core.i2c import MockBus


BME280_I2C_DATA_IN = [
    [104, 110, 232, 100, 50, 0, 83, 143, 171, 213, 208, 11, 163, 34, 53, 0, 249, 
        255, 172, 38, 10, 216, 189, 16, 0, 75],
    [108, 1, 0, 19, 10, 0, 30],
    [86, 133, 0],
    [126, 87, 0],
    [116, 223]
]

BME280_CALIB_DATA = {
    'T1': 28264, 'T2': 25832, 'T3': 50, 'P1': 36691, 'P2': -10837, 
    'P3': 3024, 'P4': 8867, 'P5': 53, 'P6': -7, 'P7': 9900, 'P8': -10230, 
    'P9': 4285, 'H1': 75, 'H2': 364, 'H3': 0, 'H4': 314, 'H5': 0, 'H6': 30
}

def test_create_bme280():
    bus = MockBus(read_data=BME280_I2C_DATA_IN)
    sensor = BME280(bus=bus)
    assert sensor
    return sensor

def test_calibration_data_bme280():
    sensor = test_create_bme280()
    for key, value in BME280_CALIB_DATA.items():
        assert sensor.calibration_data[key] == value

def test_measure_bme280():
    sensor = test_create_bme280()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['humidity'] - 54.88 <= 0.1
    assert sensor_data['temperature'] - 20.08 <= 0.1
    assert sensor_data['pressure'] - 93245.52 <= 0.1

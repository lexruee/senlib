# -*- coding: utf-8 -*-
from senlib.i2c.sensors.bmpx import BMP180
from senlib.i2c.sensors.bmpx import BMP280
from senlib.core.i2c import MockBus


BMP180_I2C_DATA_IN = [
    85,
    [27, 103, 251, 151, 199, 52, 127, 144, 97, 164, 65, 238, 25, 115, 0, 42, 
        128, 0, 209, 246, 11, 6],
    [100, 11],
    [145, 157, 128]
]
BMP280_I2C_DATA_IN = [
    [30, 109, 97, 103, 24, 252, 147, 140, 255, 213, 208, 11, 160, 15, 139, 
        0, 249, 255, 140, 60, 248, 198, 112, 23, 0, 0],
    [108, 153, 0],
    [124, 227, 0]
]

BMP180_CALIB_DATA = {
    'AC1': 7015, 'AC2': -1129, 'AC3': -14540, 'AC4': 32656, 'AC5': 24996,
    'AC6': 16878, 'B1': 6515, 'B2': 42, 'MB': -32768, 'MC': -11786, 'MD': 2822
}
BMP280_CALIB_DATA = {
    'T1': 27934, 'T2': 26465, 'T3': -1000, 'P1': 35987, 'P2': -10753, 
    'P3': 3024, 'P4': 4000, 'P5': 139, 'P6': -7, 'P7': 6000, 'P8': -14600, 
    'H1': 0
}

def test_create_bmp180():
    bus = MockBus(read_data=BMP180_I2C_DATA_IN)
    sensor = BMP180(bus=bus)
    assert sensor
    return sensor

def test_calibration_data_bmp180():
    sensor = test_create_bmp180()
    print(sensor.calibration_data)
    for key, value in BMP180_CALIB_DATA.items():
        assert sensor.calibration_data[key] == value

def test_measure_bmp180():
    sensor = test_create_bmp180()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 25.7 <= 0.1
    assert sensor_data['pressure'] -  92829 <= 0.1

def test_close_bmp180():
    sensor = test_create_bmp180()
    sensor_data = sensor.measure()
    sensor.close() 

def test_create_bmp280():
    bus = MockBus(read_data=BMP280_I2C_DATA_IN)
    sensor = BMP280(bus=bus)
    assert sensor
    return sensor

def test_calibration_data_bmp280():
    sensor = test_create_bmp280()
    print(sensor.calibration_data)
    for key, value in BMP280_CALIB_DATA.items():
        assert sensor.calibration_data[key] == value

def test_measure_bmp280():
    sensor = test_create_bmp280()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] - 20.33 <= 0.1
    assert sensor_data['pressure'] - 92966.48 <= 0.1

def test_close_bmp280():
    sensor = test_create_bmp280()
    sensor_data = sensor.measure()
    sensor.close() 

# -*- coding: utf-8 -*-
from senlib.i2c.sensors.mcpx import MCP9808
from senlib.core.i2c import MockBus

I2C_DATA_IN = [
    4,
    16833,
    17089,
    17601
]


def test_create_mcp9808():
    bus = MockBus(read_data=I2C_DATA_IN)
    sensor = MCP9808(bus=bus)
    assert sensor
    return sensor

def test_measure_mcp9808():
    sensor = test_create_mcp9808()
    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.0625

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.125

    sensor_data = sensor.measure()
    assert sensor_data
    assert sensor_data['temperature'] == 20.25

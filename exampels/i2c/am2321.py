#!/usr/bin/env python3
from senlib.core.i2c import Controller
from senlib.i2c.sensors.amx import AM2321
import time

if __name__ == '__main__':
    i2c_ctrl = Controller(bus=1)
    sensor = AM2321(i2c_ctrl=i2c_ctrl)
    time.sleep(0.2)
    data = sensor.measure()
    print(data)
    time.sleep(0.2)

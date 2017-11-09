#!/usr/bin/env python3
from senlib.core.i2c import SMBus
from senlib.i2c.sensors.mplx import MPL3115A2
import time

if __name__ == '__main__':
    i2c_ctrl = SMBus(bus=1)
    sensor = MPL3115A2(i2c_ctrl=i2c_ctrl)
    time.sleep(0.2)
    data = sensor.measure()
    print(data)
    time.sleep(0.2)

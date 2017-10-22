#!/usr/bin/env python3
from senlib.core.i2c import Controller
from senlib.i2c.sensors.six import SI7021
import time

if __name__ == '__main__':
    i2c_ctrl = Controller(bus=1)
    si = SI7021(i2c_ctrl=i2c_ctrl)
    time.sleep(0.2)
    data = si.measure()
    print(data)
    time.sleep(0.2)

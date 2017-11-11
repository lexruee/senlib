#!/usr/bin/env python3
from senlib.core.i2c import SMBus
from senlib.i2c.sensors.lmx import LM75
import time

if __name__ == '__main__':
    bus = SMBus(bus=1)
    sensor = LM75(bus=bus)
    time.sleep(0.2)
    data = sensor.measure()
    print(data)
    time.sleep(0.2)

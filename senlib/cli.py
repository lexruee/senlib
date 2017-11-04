# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import argparse

def main():
    parser = argparse.ArgumentParser(description='senlib CLI')
    parser.add_argument('sensor', help='I2C sensor')
    parser.add_argument('-a', '--addr', type=str, dest='addr', help='I2C address')
    parser.add_argument('-b', '--bus', type=int, dest='bus', help='I2C bus')
    parser.add_argument('-d', '--debug', dest='debug', help='debug',
            action='store_true')
    parser.add_argument('--mock', dest='mock', help='mock', action='store_true')
    parser.add_argument('--http', dest='http', help='Run HTTP server',
            action='store_true')
    parser.add_argument('--http-address', type=str, dest='http_address', help='HTTP address', default='0.0.0.0')
    parser.add_argument('--http-port', type=int, dest='http_port', help='HTTP port', default=8080)
    args = parser.parse_args()

    if args.debug:
        import logging
        logger = logging.getLogger('senlib')
        logging.basicConfig(level=logging.DEBUG)

    try:
        from senlib.i2c import get_sensor
        from senlib.i2c import DriverNotFound
        from collections import OrderedDict

        addr = args.addr
        if addr:
            addr = int(addr, 0)

        sensor = None
        if args.mock:
            from senlib.mock import Sensor
            sensor = Sensor()
        else:
            sensor = get_sensor(name=args.sensor, bus=args.bus, addr=addr)
        
        print("sensor: {}".format(args.sensor.lower()))
        for key, value in OrderedDict(sorted(sensor.measure().items())).items():
            print("\t{}: {}".format(key, value))
        print('')
        
        if args.http:
            from senlib.http import Server
            server = Server(sensor)
            server.run(args.http_address, args.http_port)

    except DriverNotFound as e:
        print(e)


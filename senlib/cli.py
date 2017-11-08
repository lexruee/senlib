# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

from collections import OrderedDict
import argparse
from .__version__ import __version__
import json
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='senlib CLI - Quick and dirty'
            ' CLI for using some I2C sensors.')
    parser.add_argument('--version', action='version', version='%(prog)s {}'
            .format(__version__), help='Print version number.')
    
    parser.add_argument('sensor', help='Set I2C sensor driver.')
    parser.add_argument('--mock', dest='mock', help='Use a mock sensor.', 
            action='store_true')

    parser.add_argument('-a', '--address', type=str, dest='addr', 
        help='Set I2C address.')
    parser.add_argument('-b', '--bus', type=int, dest='bus', help='Set I2C bus.', 
            default=1)
    parser.add_argument('-d', '--debug', dest='debug', help='Start debug mode.',
            action='store_true')
  
    parser.add_argument('-p', '--poll', type=int, dest='poll', nargs='?', 
            action='store', help='Start polling loop.', default=1)
    parser.add_argument('-i', '--interval', type=float, dest='interval', 
            help='Set sampling interval.', default=2)

    parser.add_argument('-f', '--format', type=str, dest='format', 
            help='Set output format.', choices=['json', 'xml', 'txt'], 
            default='txt')
    parser.add_argument('--pretty-print', dest='pretty_print', 
        help='Use pretty print output format.', action='store_true')
    parser.add_argument('-o', '--output', type=str, dest='output', 
            help='Save output to a file.')

    parser.add_argument('--http', dest='http', help='Run an HTTP server.',
            action='store_true')
    parser.add_argument('--http-address', type=str, dest='http_address', 
            help='Set HTTP address.', default='0.0.0.0')
    parser.add_argument('--http-port', type=int, dest='http_port', 
            help='Set HTTP port.', default=8080)
    args = parser.parse_args()

    import logging
    from senlib.i2c import DriverNotFound
    from senlib.i2c import get_sensor_driver
    from senlib.core.i2c import LogController
    from senlib.core.i2c import Controller

   
    try:
        addr = int(args.addr, 0) if args.addr else None
        args.output_file = open(args.output, 'w+') if args.output else None

        i2c_ctrl = None
        if args.debug:
            logger = logging.getLogger('senlib')
            logging.basicConfig(level=logging.DEBUG)
            i2c_ctrl = LogController(bus=args.bus)
        else:
            i2c_ctrl = Controller(bus=args.bus)
     
        sensor = None
        if args.mock:
            from senlib.mock import Sensor
            sensor = Sensor()
        else:
            driver_class = get_sensor_driver(name=args.sensor)
            sensor = driver_class(i2c_ctrl, addr or driver_class.default_addr())

        if args.http:
            from senlib.http import Server
            server = Server(sensor)
            server.run(args.http_address, args.http_port)
        else:
            import asyncio
            loop = asyncio.get_event_loop()
            def callback(num):
                sensor_data = sensor.measure()
                generate_output(args, sensor, sensor_data)
                if num != args.poll:
                    loop.call_later(args.interval, callback, num+1)
                else:
                    loop.stop()

            try:
                loop.call_soon(callback, 1)
                loop.run_forever()
            except KeyboardInterrupt:
                pass
            finally:
                loop.close()
                if args.output_file:
                    args.output_file.close()

    except DriverNotFound as e:
        print(e)

def generate_output(args, sensor, sensor_data):
    data = OrderedDict()
    data['name'] = args.sensor.lower()
    data['timestamp'] = str(datetime.now())
    data['measurements'] = {}
    for key, value in sorted(sensor_data.items()):
       data['measurements'][key] = value

    out = ''
    if args.format == 'json':
        out = generate_json(args, data)
    elif args.format == 'xml':
        out = generate_xml(args, data)
    else:
        out = generate_text(args, data)

    print(out)
    if args.output_file:
        args.output_file.write(out)

def generate_json(args, data):
    indent = 4 if args.pretty_print else None
    json_data = json.dumps(data, indent=indent)
    return json_data

def generate_xml(args, data):
    xml = dicttoxml(data, attr_type=False, custom_root='sensor')
    if args.pretty_print:
        dom = parseString(xml)
        return dom.toprettyxml()
    else:
        return xml

def generate_text(args, data):
    out = "sensor: {}\n".format(data['name'])
    out += "timestamp: {}\n".format(data['timestamp'])
    for key, value in data['measurements'].items():
        out += "\t{}: {}\n".format(key, value)
    return out

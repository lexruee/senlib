# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import asyncio
import time
import sys
import logging
import platform
import json
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
from datetime import datetime

from collections import namedtuple
from collections import OrderedDict

from senlib import logger
from senlib.mock import Sensor as MockSensor
from senlib.i2c import DriverNotFound
from senlib.i2c import get_sensor_driver
from senlib.core.i2c import SMBus, AddressParser
from senlib.web import WebServer
from senlib.mqtt import Publisher


class AsyncioApp:
    """ Base class for Asyncio-based CLI applications. """

    def __init__(self, config, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._config = self.create_config(config)
        self._sensor = None

        if self._config.debug:
            logging.basicConfig(level=logging.DEBUG)
  
        self._sensor = self.create_sensor()

        self._after_init()
    
    def create_config(self, config_dict):
        """ Creates a Config object. """

        Config = namedtuple('Config', list(config_dict.keys()))
        return Config(**config_dict)

    def create_sensor(self):
        """ Creates a sensor object. """
        sensor = None
        if self._config.mock:
            sensor = MockSensor()
        else:
            i2c_bus, i2c_addr = AddressParser().parse(self._config.address)
            i2c_ctrl = SMBus(bus=i2c_bus)
            driver_class = get_sensor_driver(name=self._config.sensor)
            sensor = driver_class(i2c_ctrl, i2c_addr or driver_class.default_addr())
        return sensor

    def _after_init(self): 
        """ Internal template method. """
        pass

    def _start(self): 
        """ Internal template method. """
        pass

    def _before_start(self):
        """ Internal template method. """
        pass

    def _after_start(self):
        """ Internal template method. """
        pass

    def _after_stop(self):
        """ Internal template method. """
        pass

    def run(self):
        """  Runs the Async application. """
        self._before_start()
        self._start()
        try:
           self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._after_stop()


class SenlibCli(AsyncioApp):
    """ SenlibCli is an Asyncio-based CLI application. """

    def _generate_output(self, sensor, sensor_data):
        data = OrderedDict()
        data['name'] = self._config.sensor.lower()
        data['timestamp'] = str(datetime.now())
        data['measurements'] = {}
        for key, value in sorted(sensor_data.items()):
           data['measurements'][key] = value

        out = ''
        if self._config.format == 'json':
            out = self._generate_json(data)
        elif self._config.format == 'xml':
            out = self._generate_xml(data)
        else:
            out = self._generate_text(data)

        return out

    def _generate_json(self, data):
        """ Generates JSON output. """
        indent = 4 if self._config.pretty_print else None
        json_data = json.dumps(data, indent=indent)
        return json_data

    def _generate_xml(self, data):
        """ Generates XML output. """
        xml = dicttoxml(data, attr_type=False, custom_root='sensor')
        if self._config.pretty_print:
            dom = parseString(xml)
            return dom.toprettyxml()
        else:
            return xml

    def _generate_text(self, data):
        """ Generates plain text output. """
        out = "timestamp: {}\n".format(data['timestamp'])
        for key, value in data['measurements'].items():
            out += "{}: {}\n".format(key, value)
        return out

    def _start(self):
        def callback(num):
            sensor_data = self._sensor.measure()
            print(self._generate_output(self._sensor, sensor_data))

            if num != self._config.poll:
                self._loop.call_later(self._config.interval, callback, num+1)
            else:
                self._loop.stop()
                    
        self._loop.call_soon(callback, 1)


class SennodeCli(AsyncioApp):
    """ SennodeCLI is an Asyncio-based CLI sensor node application. """

    def _after_init(self):
        self._webserver = None
        self._publisher = None

        if self._config.http:
            self._webserver = WebServer(self._config.interval, self._loop, self._sensor)

        if self._config.mqtt_broker_url:
            self.mqtt_topic = self._config.mqtt_topic
            if not self.mqtt_topic:
                self.mqtt_topic = 'sensor/{}'.format(self._sensor.DRIVER_NAME)

            self._publisher = Publisher(self._config.mqtt_broker_url, self.mqtt_topic)

    def _publish_data(self, data):
        data['timestamp'] = time.time()
        data['node'] = self._config.node or platform.node()
        if self._webserver:
            self._webserver.broadcast(data)
        
        if self._publisher:
            self._publisher.publish(data)

    def _start(self):
        print("Enter Ctrl-C to exit.")

        if self._webserver:
            print("HTTP server runs under http://{}:{}".format(self._config.http_host, 
                self._config.http_port))
            print("Websocket server runs under ws://{}:{}".format(self._config.http_host, 
                self._config.http_port))

            h = self._webserver.make_handler()
            f = self._loop.create_server(h, self._config.http_host, self._config.http_port)
            self._loop.run_until_complete(f)

        if self._publisher:
            async def connect():
                code = await self._publisher.connect()
                if code == 0:
                    print("Connected to MQTT broker {}".format(self._config.mqtt_broker_url))
                    print("Publish data under topic {}".format(self.mqtt_topic))

            asyncio.ensure_future(connect())

        def callback():
            logger.debug('callback')
            sensor_data = self._sensor.measure()
            self._publish_data(sensor_data)
            self._loop.call_later(self._config.interval, callback)
                        
        self._loop.call_soon(callback)


    def _after_stop(self):
        if self._publisher:
            self._publisher.disconnect()


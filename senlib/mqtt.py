# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import asyncio
from senlib import logger
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
import json


class Publisher:

    def __init__(self, broker, port, topic):
        self._broker = broker
        self._port = port
        self._topic = topic
        self._client = MQTTClient()
        asyncio.ensure_future(self._client.connect('{}:{}'.format(self._broker,
            self._port)))

    def publish(self, data):
        json_data = json.dumps(data)
        bdata = bytes(json_data, 'utf-8')
        asyncio.ensure_future(self._client.publish(self._topic, bdata))

    def close(self):
        self._client.disconnect()

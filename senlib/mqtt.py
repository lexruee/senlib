# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import asyncio
from senlib import logger
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
import json
import time

class Publisher:

    def __init__(self, broker, port, topic):
        self._broker = broker
        self._port = port
        self._topic = topic
        self._client = MQTTClient()
        self._connection_code = None
                
    async def connect(self):
        self._connection_code = await self._client.connect('{}:{}'.format(self._broker, self._port))
        return self._connection_code

    def publish(self, data):
        data['timestamp'] = time.time()
        json_data = json.dumps(data)
        bdata = bytes(json_data, 'utf-8')
        if self._connection_code == 0x00:
            asyncio.ensure_future(self._client.publish(self._topic, bdata))

    def disconnect(self):
        self._client.disconnect()

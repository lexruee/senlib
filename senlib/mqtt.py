# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import asyncio
from senlib import logger
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
import json
import logging
logger = logging.getLogger('mqtt')


class Publisher:

    def __init__(self, broker_url, topic):
        self._broker_url = broker_url
        self._topic = topic
        self._client = MQTTClient()
        self._connection_code = None
                
    async def connect(self):
        logger.debug('connect')
        self._connection_code = await self._client.connect(self._broker_url)
        return self._connection_code

    def publish(self, data):
        logger.debug('publish data: {}'.format(data))
        json_data = json.dumps(data)
        bdata = bytes(json_data, 'utf-8')
        if self._connection_code == 0x00:
            asyncio.ensure_future(self._client.publish(self._topic, bdata))

    def disconnect(self):
        logger.debug('disconnect')
        self._client.disconnect()

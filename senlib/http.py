# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

from aiohttp import web
import json

class Server(object):

    def __init__(self, sensor):
        self._sensor = sensor
        self._app = web.Application()
        self._app.router.add_get('/', self._handle)

    async def _handle(self, request):
        data = self._sensor.measure()
        return web.Response(body=json.dumps(data, indent=4, separators=(',', ': ')).encode('utf-8'),
                content_type='application/json')

    def run(self, host, port):
        web.run_app(self._app, host=host, port=port)

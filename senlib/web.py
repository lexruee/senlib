# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import aiohttp
import asyncio
from aiohttp import web
from senlib import logger
import time


class WebServer:

    def __init__(self, interval, loop, sensor):
        self._loop = loop
        self._handler = Handler(interval, self._loop, sensor)
        self._app = web.Application()
        self._app.router.add_get('/', self._handler.index)

    def run(self, host='0.0.0.0', port=8080):
        web.run_app(self._app, host=host, port=port)

    def make_handler(self):
        return self._app.make_handler()

    def broadcast(self, data):
        asyncio.ensure_future(self._handler.broadcast(data))


class Handler:

    def __init__(self, interval, loop, sensor):
        self._interval = interval
        self._loop = loop
        self._sensor = sensor
        self._clients = []

    def _create_data(self):
        data = self._sensor.measure()
        data['timestamp'] = time.time()
        return data

    async def broadcast(self, data):
        for ws in self._clients:
            await ws.send_json(data)
    
    async def index(self, request):
        ws = web.WebSocketResponse(timeout=5)
        try: 
            logger.debug('try to upgrade to websocket protocol')
            ws.can_prepare(request)
            await ws.prepare(request)
            self._clients.append(ws)

            while True:
                await asyncio.sleep(self._interval)
                logger.debug('alive...')
                logger.debug(self._clients)

        except web.HTTPException as e:
            logger.debug('cannot upgrade to websocket protocol')
            data = self._create_data()
            if 'Accept' in request.headers:
                if 'application/json' in request.headers['Accept']:
                    return web.json_response(data)
                else:
                    return web.json_response(data)
            return web.json_response(data)

        except Exception as e:
            logger.debug(e)
            logger.debug('websocket connection closed')
            if ws in self._clients:
                self._clients.remove(ws)
            return ws


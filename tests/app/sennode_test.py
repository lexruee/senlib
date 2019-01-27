# -*- coding: utf-8 -*-
from senlib.app import SennodeApp


def test_create_sennnodeapp():
    config = {
            'debug': False,
            'mock': True,
            'http': True,
            'interval': 1.0,
            'mqtt_broker_url': None,
    }
    app = SennodeApp(config)
    assert app is not None


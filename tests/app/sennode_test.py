# -*- coding: utf-8 -*-
from senlib.app import SennodeCli


def test_create_sennnodecli():
    config = {
            'debug': False,
            'mock': True,
            'http': True,
            'interval': 1.0,
            'mqtt_broker_url': None,
    }
    cli = SennodeCli(config)
    assert cli is not None


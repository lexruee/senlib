# -*- coding: utf-8 -*-
from senlib.app import SenlibApp


def test_create_senlibapp():
    config = {
            'debug': False,
            'mock': True,
            'interval': 1.0,
    }
    app = SenlibApp(config)
    assert app is not None


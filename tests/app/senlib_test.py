# -*- coding: utf-8 -*-
from senlib.app import SenlibCli


def test_create_senlibcli():
    config = {
            'debug': False,
            'mock': True,
            'interval': 1.0,
    }
    cli = SenlibCli(config)
    assert cli is not None


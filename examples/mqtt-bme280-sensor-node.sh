#!/usr/bin/env bash

sennode bme280 i2c://1/0x77 \
    --mqtt-url ws://zeus.local \
    -i 5 -t 'home/og1/bme280'

# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import logging
import click
from .app import SenlibApp 
from .app import SennodeApp
from .__version__ import __version__

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit() 


@click.command()
@click.argument('sensor')
@click.option('--address', help='I2C address of the sensor.')
@click.option('--poll', '-p', default=1, help='Polls the sensor.')
@click.option('--interval','-i', default=2.0, help='Sampling interval.')
@click.option('--output', type=click.File('w'), help='Save output to a file.')
@click.option('--format','-f', help='Output format to use.')
@click.option('--mock','--fake','--simulate', is_flag=True, help='Mock sensor.')
@click.option('--debug', '-d', is_flag=True, help='Debug mode.')
@click.option('--pretty-print', '--pp', is_flag=True, help='Pretty printing.')
@click.option('--version', '-V', is_flag=True, callback=print_version, 
        expose_value=False, is_eager=True, help='Show version.')
def senlib(**kwargs):
    app = SenlibApp(kwargs)
    app.run()


@click.command()
@click.argument('sensor')
@click.option('--address', help='I2C address of the sensor.')
@click.option('--node', default=None, help='Node name.')
@click.option('--http', is_flag=True, help='Start Web API.')
@click.option('--http-host', default='0.0.0.0', help='HTTP host to use.')
@click.option('--http-port', default=8080, help='HTTP port to use.')
@click.option('--mqtt-topic', '-t', default=None, help='MQTT topic to use.')
@click.option('--mqtt-broker-url','-L', help='MQTT broker to publish data.')
@click.option('--interval', '-i', default=2.0, help='Sampling interval.')
@click.option('--mock','--fake','--simulate', is_flag=True, help='Mock sensor.')
@click.option('--debug', '-d', is_flag=True, help='Debug mode.')
@click.option('--version', '-V', is_flag=True, callback=print_version, 
        expose_value=False, is_eager=True, help='Show version.')
def sennode(**kwargs):
    app = SennodeApp(kwargs)
    app.run()

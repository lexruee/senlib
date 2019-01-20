# -*- coding:utf-8 -*-

__author__ = 'Alexander Rüedlinger'

import logging
import click
from .app import SenlibCli 
from .app import SennodeCli
from .__version__ import __version__

# TODO
# 1) senlib

# 2) sennide

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
    app = SenlibCli(kwargs)
    app.run()


@click.command()
@click.argument('sensor')
@click.option('--address', help='I2C address of the sensor.')
@click.option('--http', is_flag=True, help='Start Web API.')
@click.option('--http-port', help='HTTP port to use.')
@click.option('--mqtt', is_flag=True, help='Start MQTT broker.')
@click.option('--mqtt-port', help='MQTT port to use.')
@click.option('--mqtt-broker-url', help='MQTT broker to publish data.')
@click.option('--interval', '-i', default=2.0, help='Sampling interval.')
@click.option('--mock','--fake','--simulate', is_flag=True, help='Mock sensor.')
@click.option('--debug', '-d', is_flag=True, help='Debug mode.')
@click.option('--version', '-V', is_flag=True, callback=print_version, 
        expose_value=False, is_eager=True, help='Show version.')
def sennode(**kwargs):
    app = SennodeCli(kwargs)
    click.echo('TODO')
    #app.run()

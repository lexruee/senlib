senlib
======

Installation
------------

::

   git clone https://github.com/lexruee/senlib
   cd senlib
   ./setup.py

CLI
---

sennode
~~~~~~~

::

   sennode --help
   usage: sennode [-h] [--version] [--mock] [-a ADDR] [-b BUS] [-d] [-i INTERVAL]
                  [--http-address HTTP_ADDRESS] [--http-port HTTP_PORT]
                  [--mqtt-address MQTT_ADDRESS] [--mqtt-port MQTT_PORT]
                  [-t MQTT_TOPIC]
                  sensor

   sennode - Basic node application for exposing an I2C sensor via HTTP,
   WebSockets or MQTT

   positional arguments:
     sensor                Set I2C sensor driver.

   optional arguments:
     -h, --help            show this help message and exit
     --version             Print version number.
     --mock                Use a mock sensor.
     -a ADDR, --address ADDR
                           Set I2C address.
     -b BUS, --bus BUS     Set I2C bus.
     -d, --debug           Start debug mode.
     -i INTERVAL, --interval INTERVAL
                           Set sampling interval.
     --http-address HTTP_ADDRESS
                           Set HTTP address.
     --http-port HTTP_PORT
                           Set HTTP port.
     --mqtt-address MQTT_ADDRESS
                           Set MQTT broker address.
     --mqtt-port MQTT_PORT
                           Set MQTT broker port.
     -t MQTT_TOPIC, --mqtt-topic MQTT_TOPIC
                           Set MQTT topic.

.. _senlib-1:

senlib
~~~~~~

::

   senlib --help
   usage: senlib [-h] [--version] [--mock] [-a ADDR] [-b BUS] [-d] [-p [POLL]]
                 [-i INTERVAL] [-f {json,xml,txt}] [--pretty-print] [-o OUTPUT]
                 sensor

   senlib - Basic CLI for retrieving data for some I2C sensors.

   positional arguments:
     sensor                Set I2C sensor driver.

   optional arguments:
     -h, --help            show this help message and exit
     --version             Print version number.
     --mock                Use a mock sensor.
     -a ADDR, --address ADDR
                           Set I2C address.
     -b BUS, --bus BUS     Set I2C bus.
     -d, --debug           Start debug mode.
     -p [POLL], --poll [POLL]
                           Start polling loop.
     -i INTERVAL, --interval INTERVAL
                           Set sampling interval.
     -f {json,xml,txt}, --format {json,xml,txt}
                           Set output format.
     --pretty-print        Use pretty print output format.
     -o OUTPUT, --output OUTPUT
                           Save output to a file.

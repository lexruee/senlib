senlib
======

Pure Python-based I2C sensor library for some I2C sensors. Work in
progress. Nothing serious, just a hobby.

Currently, the library supports the following sensors:

-  am2315/am2321
-  bh1750
-  bmp280/bmp180/bmp85
-  bme280
-  hdc1008
-  lm75
-  mcp9808
-  mpl115a2
-  mpl311a2
-  sht31
-  si7021

Installation
------------

::

   git clone https://github.com/lexruee/senlib
   cd senlib
   ./setup.py

Testing/Development
-------------------

::

   pipenv --three
   pipenv shell
   git clone https://github.com/lexruee/senlib
   cd senlib
   pip install -e .
   pytest tests

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

Example Usage
^^^^^^^^^^^^^

::

   sennode bme280 -a 0x77 -b 1

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

.. _example-usage-1:

Example Usage
^^^^^^^^^^^^^

::

   senlib bme280 -a 0x77 -b 1 -p -i 1

Code Examples
-------------

For details and examples have a look in the examples or tests directory.

Basic code example:

.. code:: python

   #!/usr/bin/env python3
   from senlib.core.i2c import SMBus
   from senlib.i2c.sensors.bmex import BME280
   import time

   if __name__ == '__main__':
       bus = SMBus(bus=1)
       sensor = BME280(bus=bus, addr=0x77)
       for _ in range(0, 5):
          time.sleep(0.2)
          data = sensor.measure()
          for key, value in data.items():
              print("{}:{:0.4f}".format(key, value))
          
       sensor.close()

The shorter example uses the ``with`` syntax to automatically close the
sensor object:

.. code:: python

   #!/usr/bin/env python3
   from senlib.core.i2c import SMBus
   from senlib.i2c.sensors.bmex import BME280
   import time

   if __name__ == '__main__':
       bus = SMBus(bus=1)
       with BME280(bus=bus, addr=0x77) as sensor:
          for _ in range(0, 5):
              time.sleep(0.2)
              data = sensor.measure()
              for key, value in data.items():
                  print("{}:{:0.4f}".format(key, value))

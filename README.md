# senlib

Pure Python-based I2C sensor library for some I2C sensors. Work in progress. 
Nothing serious, just a hobby.

Currently, the library supports the following sensors:

 * am2315/am2321
 * bh1750
 * bmp280/bmp180/bmp85
 * bme280
 * hdc1008
 * lm75
 * mcp9808
 * mpl115a2
 * mpl311a2
 * sht31
 * si7021


## Installation

Before you can install senlib, you should install first `pipenv` using
the package manager of your operating system.

On Arch Linux run the following command to install `pipenv`:

```
sudo pacman -S python-pipenv
```

Next, clone this repo and cd into the `senlib` directory:

```
git clone https://github.com/lexruee/senlib
cd senlib
```

Next, create a Python 3 environment as shown below:

```
pipenv --three
```

Lastly, install the package:

```
pipenv install -e .
```

## Testing/Development

For installation see section Installation.

To run the tests use:

```
pipenv run pytest tests
```

or cd into the directory and run:

```
pipenv shell && pytest tests
```


## CLI

### sennode

```
sennode --help
Usage: sennode [OPTIONS] SENSOR

Options:
  --address TEXT              I2C address of the sensor.
  --node TEXT                 Node name.
  --http                      Start Web API.
  --http-host TEXT            HTTP host to use.
  --http-port INTEGER         HTTP port to use.
  -t, --mqtt-topic TEXT       MQTT topic to use.
  --mqtt-broker-url TEXT      MQTT broker to publish data.
  -i, --interval FLOAT        Sampling interval.
  --mock, --fake, --simulate  Mock sensor.
  -d, --debug                 Debug mode.
  -V, --version               Show version.
  --help                      Show this message and exit.
```


#### Example Usage

```
sennode bme280 --address 'i2c://1/0x77' --mqtt-broker-url mqtts://user:password@mqtt.xyz.ch:8883
```

Once started, the sensor data is exposed over an HTTP interface and
a WebSocket interface:

 * http://0.0.0.0:8080
 * ws://0.0.0.0:8080

Besides that, the sensor data is perodically pushlished to the specified
MQTT broker url.


### senlib

```
senlib --help
Usage: senlib [OPTIONS] SENSOR

Options:
  --address TEXT              I2C address of the sensor.
  -p, --poll INTEGER          Polls the sensor.
  -i, --interval FLOAT        Sampling interval.
  --output FILENAME           Save output to a file.
  -f, --format TEXT           Output format to use.
  --mock, --fake, --simulate  Mock sensor.
  -d, --debug                 Debug mode.
  --pretty-print, --pp        Pretty printing.
  -V, --version               Show version.
  --help                      Show this message and exit.
```

#### Example Usage

```
senlib bme280 --address 'i2c://1/0x77'
```

## Code Examples

For details and examples have a look in the examples or tests directory.

Basic code example:

```python
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
```

The shorter example uses the `with` syntax to automatically close the sensor object:

```python
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
```




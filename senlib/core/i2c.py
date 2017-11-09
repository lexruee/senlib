# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('SMBus')

import struct
import fcntl
import io
from collections import deque
import logging
logger = logging.getLogger('i2c')


class SMBusInterface(object):
    """
    A helper class for using the Linux SMBus interface.
    """

    @property
    def name(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self

    def read_byte(self, addr):
        raise NotImplementedError

    def write_byte(self, addr, val):
        raise NotImplementedError

    def read_byte_data(self, addr, cmd):
        raise NotImplementedError

    def write_byte_data(self, addr, cmd, val):
        raise NotImplementedError

    def read_word_data(self, addr, cmd):
        raise NotImplementedError

    def write_block_data(self, cmd, vals):
        raise NotImplementedError

    def read_i2c_block_data(self, addr, cmd, nbytes):
        raise NotImplementedError

    def write_i2c_block_data(self, addr, cmd, vals):
        raise NotImplementedError

    def __str__(self):
        return '<{}(name={})>'.format(self.__class__.__name__, self.name)

    __repr__ = __str__


class I2CInterface(object):
    """
    A helper class for using the Linux I2C interface.
    """

    @property
    def name(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self

    def read_byte(self, addr):
        raise NotImplementedError

    def write_byte(self, addr, val):
        raise NotImplementedError

    def read_byte_data(self, addr, cmd):
        raise NotImplementedError

    def write_byte_data(self, addr, cmd, val):
        raise NotImplementedError

    def read_word_data(self, addr, cmd):
        raise NotImplementedError

    def write_block_data(self, cmd, vals):
        raise NotImplementedError

    def read_i2c_block_data(self, addr, cmd, nbytes):
        raise NotImplementedError

    def write_i2c_block_data(self, addr, cmd, vals):
        raise NotImplementedError

    def __str__(self):
        return '<{}(name={})>'.format(self.__class__.__name__, self.name)

    __repr__ = __str__


class SMBus(SMBusInterface):
    """
    A helper class for using the Linux I2C/SMBus interface.
    """

    def __init__(self, bus=1, SMBus=None):
        self._bus = bus
        self._smbus = None
        if SMBus is not None:
            self._smbus = SMBus(bus)
        else:
            import smbus
            self._smbus = smbus.SMBus(bus)

        msg = 'create SMBus(bus={}) object'.format(bus)
        logger.debug(msg)

    @property
    def name(self):
        return 'i2c-{}'.format(self._bus)

    @property
    def bus(self):
        return self._bus

    def close(self):
        self._smbus.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self

    def read_byte(self, addr):
        r = self._smbus.read_byte(addr)
        msg = 'call SMBus.read_byte(addr={})={}'.format(addr, r)
        logger.debug(msg)
        return r

    def write_byte(self, addr, val):
        msg = 'call SMBus.write_byte(addr={}, val={})'.format(addr, val)
        logger.debug(msg)
        self._smbus.write_byte(addr, val)

    def read_byte_data(self, addr, cmd):
        r = self._smbus.read_byte_data(addr, cmd)
        msg = 'call SMBus.read_byte_data(addr={}, cmd={})={}'.format(addr, cmd, r)
        logger.debug(msg)
        return r

    def write_byte_data(self, addr, cmd, val):
        msg = 'call SMBus.write_byte_data(addr={}, cmd={}, val={})'.format(addr, cmd, val)
        logger.debug(msg)
        self._smbus.write_byte_data(addr, cmd, val)

    def read_word_data(self, addr, cmd):
        r = self._smbus.read_word_data(addr, cmd)
        msg = 'call SMBus.read_word_data(addr={}, cmd={})={}'.format(addr, cmd, r)
        logger.debug(msg)
        return r

    def write_word_data(self, addr, cmd, val):
        msg = 'call SMBus.write_word_data(addr={}, cmd={}, val={})'.format(addr, 
                cmd, val)
        logger.debug(msg)
        self._smbus.write_word_data(addr, cmd, val)

    def read_i2c_block_data(self, addr, cmd, nbytes):
        r = self._smbus.read_i2c_block_data(addr, cmd, nbytes)
        msg = 'call SMBus.read_i2c_block_data(addr={}, cmd={}, nbytes={})={}'.format(addr, cmd, nbytes, r)
        logger.debug(msg)
        return r

    def write_i2c_block_data(self, addr, cmd, vals):
        msg = 'call SMBus.write_i2c_block_data(addr={}, cmd={}, vals={})'.format(addr, cmd, vals)
        logger.debug(msg)
        self._smbus.write_i2c_block_data(addr, cmd, vals)


class MockBus(SMBusInterface, I2CInterface):
    """
    A helper class for mocking the Linux I2C/SMBus interface.
    """

    def __init__(self, bus=1, SMBus=None, read_data=None):
        self._bus = bus
        self._read_data = deque(read_data or [])

    @property
    def name(self):
        return 'i2c-{}'.format(self._bus)

    @property
    def bus(self):
        return self._bus

    def close(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __enter__(self):
        return self

    def read_byte(self, addr):
        return self._read_data.popleft()

    def write_byte(self, addr, val):
        pass

    def read_byte_data(self, addr, cmd):
        return self._read_data.popleft()

    def write_byte_data(self, addr, cmd, val):
        pass

    def read_word_data(self, addr, cmd):
        return self._read_data.popleft()

    def write_word_data(self, addr, cmd, val):
        pass

    def read_i2c_block_data(self, addr, cmd, nbytes):
        return self._read_data.popleft()

    def write_i2c_block_data(self, addr, cmd, vals):
        pass


class Device(object):

    def __init__(self, bus, addr):
        self._bus = bus
        self._addr = addr

    @property
    def name(self):
        return self.create_device_id(self.driver_name, self._bus.name, self.addr)

    @property
    def bus(self):
        return self._bus

    @classmethod
    def driver_name(cls):
        raise NotImplementedError

    @classmethod
    def default_addr(cls):
        raise NotImplementedError

    @property
    def addr(self):
        return self._addr

    @staticmethod
    def create_device_id(driver_name, bus_name, addr):
        # return a string such as /i2c-1/bmp280@0x77
        return '/{}/{}@0x{:x}'.format(bus_name, driver_name, addr)

    def close(self):
        self._i2c_ctrl.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self

    def __str__(self):
        return '<{}(ctrl={},addr=0x{:x},name={})>'.format(self.__class__.__name__,
            self._bus.name, self._addr, self.name)

    __repr__ = __str__


class Sensor(Device):
    """
    Basic generic interface of the supported sensors.
    """

    def __init__(self, bus, addr):
        super(Sensor, self).__init__(bus, addr)

    def measure(self):
        return {}

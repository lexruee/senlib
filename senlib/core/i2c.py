# -*- coding: utf-8 -*-

__author__ = 'Alexander Rüedlinger'
__all__ = ('Controller', 'LogController')

from collections import deque
import logging
logger = logging.getLogger('i2c')


class ControllerInterface(object):
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


class Controller(ControllerInterface):
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
        return self._smbus.read_byte(addr)

    def write_byte(self, addr, val):
        self._smbus.write_byte(addr, val)

    def read_byte_data(self, addr, cmd):
        return self._smbus.read_byte_data(addr, cmd)

    def write_byte_data(self, addr, cmd, val):
        self._smbus.write_byte_data(addr, cmd, val)

    def read_word_data(self, addr, cmd):
        return self._smbus.read_word_data(addr, cmd)

    def write_word_data(self, addr, cmd, val):
        self._smbus.write_word_data(addr, cmd, val)

    def read_i2c_block_data(self, addr, cmd, nbytes):
        return self._smbus.read_i2c_block_data(addr, cmd, nbytes)

    def write_i2c_block_data(self, addr, cmd, vals):
        self._smbus.write_i2c_block_data(addr, cmd, vals)


class LogController(ControllerInterface):
    """
    A helper class for using the Linux I2C/SMBus interface.
    """

    def __init__(self, bus=1, SMBus=None):
        self._bus = bus
        self._smbus = None
        self._log_data = []
        if SMBus is not None:
            self._smbus = SMBus(bus)
        else:
            import smbus
            self._smbus = smbus.SMBus(bus)

        msg = 'create SMBus(bus={}) object'.format(bus)
        self._log_data.append(msg)
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
        logger.debug()
        self._log_data.append(msg)
        logger.debug(msg)
        return r

    def write_byte(self, addr, val):
        msg = 'call SMBus.write_byte(addr={}, val={})'.format(addr, val)
        self._log_data.append(msg)
        logger.debug(msg)
        self._smbus.write_byte(addr, val)

    def read_byte_data(self, addr, cmd):
        r = self._smbus.read_byte_data(addr, cmd)
        msg = 'call SMBus.read_byte_data(addr={}, cmd={})={}'.format(addr, cmd, r)
        self._log_data.append(msg)
        logger.debug(msg)
        return r

    def write_byte_data(self, addr, cmd, val):
        msg = 'call SMBus.write_byte_data(addr={}, cmd={}, val={})'.format(addr, cmd, val)
        self._log_data.append(msg)
        logger.debug(msg)
        self._smbus.write_byte_data(addr, cmd, val)

    def read_word_data(self, addr, cmd):
        r = self._smbus.read_word_data(addr, cmd)
        msg = 'call SMBus.read_word_data(addr={}, cmd={})={}'.format(addr, cmd, r)
        self._log_data.append(msg)
        logger.debug(msg)
        return r

    def write_word_data(self, addr, cmd, val):
        msg = 'call SMBus.write_word_data(addr={}, cmd={}, val={})'.format(addr, 
                cmd, val)
        self._log_data.append(msg)
        logger.debug(msg)
        self._smbus.write_word_data(addr, cmd, val)

    def read_i2c_block_data(self, addr, cmd, nbytes):
        r = self._smbus.read_i2c_block_data(addr, cmd, nbytes)
        msg = 'call SMBus.read_i2c_block_data(addr={}, cmd={}, nbytes={})={}'.format(addr, cmd, nbytes, r)
        self._log_data.append(msg)
        logger.debug(msg)
        return r

    def write_i2c_block_data(self, addr, cmd, vals):
        msg = 'call SMBus.write_i2c_block_data(addr={}, cmd={}, vals={})'.format(addr, cmd, vals)
        self._log_data.append(msg)
        logger.debug(msg)
        self._smbus.write_i2c_block_data(addr, cmd, vals)


class MockController(ControllerInterface):
    """
    A helper class for mocking the Linux I2C/SMBus interface.
    """

    def __init__(self, bus=1, SMBus=None, read_data=None):
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
        return self._read_data.pop()

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

    def __init__(self, i2c_ctrl, addr):
        self._i2c_ctrl = i2c_ctrl
        self._addr = addr

    @property
    def name(self):
        return self.create_device_id(self.driver_name, self.i2c_ctrl.name, self.addr)

    @property
    def i2c_ctrl(self):
        return self._i2c_ctrl

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
    def create_device_id(driver_name, i2ctrl_name, addr):
        # return a string such as /i2c-1/bmp280@0x77
        return '/{}/{}@0x{:x}'.format(i2ctrl_name, driver_name, addr)

    def close(self):
        self._i2c_ctrl.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __enter__(self):
        return self

    def __str__(self):
        return '<{}(ctrl={},addr=0x{:x},name={})>'.format(self.__class__.__name__, self._i2c_ctrl.name, self._addr, self.name)

    __repr__ = __str__


class Sensor(Device):
    """
    Basic generic interface of the supported sensors.
    """

    def __init__(self, i2c_ctrl, addr):
        Device.__init__(self, i2c_ctrl, addr)

    def measure(self):
        return {}

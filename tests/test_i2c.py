# -*- coding: utf-8 -*-
from senlib.core.i2c import AddressParser

def test_i2c_address_parser():
    parser = AddressParser()
    assert parser is not None

    addr_tuple = parser.parse('i2c://1/0x77')
    assert addr_tuple is not None

    i2c_bus, i2c_addr = addr_tuple
    assert addr_tuple[0] == i2c_bus
    assert addr_tuple[1] == i2c_addr 

#!/usr/bin/env python3
"""
PIGPIO I2C Handle
"""
__author__ = "Daniel Casner <www.danielcasner.org>"

import pigpio

class I2C:
    "A class wrapper around and the PIGPIO I2C interface"
    
    def __init__(self, pi, *args, **kwargs):
        "Initalize the I2C handle"
        self._pi = pi
        self._handle = pi.i2c_open(*args, **kwargs)
        if self._handle < 0:
            raise IOException("Couldn't open I2C handle")
    
    def __del__(self):
        "Closes the i2c handle"
        try:
            self.close()
        except:
            pass

    def close(self):
        self._pi.i2c_close(self._handle)

    def block_process_call(self, *args, **kwargs):
        self._pi.i2c_block_process_call(self._handle, *args, **kwargs)
    def process_call(self, *args, **kwargs):
        self._pi.i2c_process_call(self._handle, *args, **kwargs)
    def read_block_data(self, *args, **kwargs):
        self._pi.i2c_read_block_data(self._handle, *args, **kwargs)
    def read_byte(self, *args, **kwargs):
        self._pi.i2c_read_byte(self._handle, *args, **kwargs)
    def read_byte_data(self, *args, **kwargs):
        self._pi.i2c_read_byte_data(self._handle, *args, **kwargs)
    def read_device(self, *args, **kwargs):
        self._pi.i2c_read_device(self._handle, *args, **kwargs)
    def read_i2c_block_data(self, *args, **kwargs):
        self._pi.i2c_read_i2c_block_data(self._handle, *args, **kwargs)
    def read_word_data(self, *args, **kwargs):
        self._pi.i2c_read_word_data(self._handle, *args, **kwargs)
    def write_block_data(self, *args, **kwargs):
        self._pi.i2c_write_block_data(self._handle, *args, **kwargs)
    def write_byte(self, *args, **kwargs):
        self._pi.i2c_write_byte(self._handle, *args, **kwargs)
    def write_byte_data(self, *args, **kwargs):
        self._pi.i2c_write_byte_data(self._handle, *args, **kwargs)
    def write_device(self, *args, **kwargs):
        self._pi.i2c_write_device(self._handle, *args, **kwargs)
    def write_i2c_block_data(self, *args, **kwargs):
        self._pi.i2c_write_i2c_block_data(self._handle, *args, **kwargs)
    def write_quick(self, *args, **kwargs):
        self._pi.i2c_write_quick(self._handle, *args, **kwargs)
    def write_word_data(self, *args, **kwargs):
        self._pi.i2c_write_word_data(self._handle, *args, **kwargs)
    def zip(self, *args, **kwargs):
        self._pi.i2c_zip(self._handle, *args, **kwargs)
    

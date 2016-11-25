# Copyright (c) 2016 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################
# Library forked and reworked to work with the pigpio library.
# Author: Daniel Casner <www.danielcasner.org>
#
from __future__ import division
from __future__ import print_function
import logging
import pigpio
from PCA9685_pigpio.pigpio_i2c import I2C
import time


# Registers/etc:
PCA9685_ADDRESS    = 0x40
MODE1              = 0x00
MODE2              = 0x01
SUBADR1            = 0x02
SUBADR2            = 0x03
SUBADR3            = 0x04
PRESCALE           = 0xFE
LED0_ON_L          = 0x06
LED0_ON_H          = 0x07
LED0_OFF_L         = 0x08
LED0_OFF_H         = 0x09
ALL_LED_ON_L       = 0xFA
ALL_LED_ON_H       = 0xFB
ALL_LED_OFF_L      = 0xFC
ALL_LED_OFF_H      = 0xFD

# Bits:
RESTART            = 0x80
SLEEP              = 0x10
ALLCALL            = 0x01
INVRT              = 0x10
OUTDRV             = 0x04
FULL_ON_OFF        = 0x1000 # Write 1 to on and 0 to off for full on or vise versa for full off

# Constants
NUM_CHANNELS       = 16
MAX_PWM            = 4095

logger = logging.getLogger(__name__)


def software_reset(i2c=None, pi=None, **kwargs):
    """Sends a software reset (SWRST) command to all servo drivers on the bus."""
    # Setup I2C interface for device 0x00 to talk to all of them.
    if i2c is None:
        if pi is None:
            pi = pigpio.pi()
        i2c = I2C(0, 0x00)
    i2c.write_device(i2c, 0x06) # SWRST

class PCA9685(object):
    """PCA9685 PWM LED/servo controller."""

    def __init__(self, address=PCA9685_ADDRESS, pi=None, i2c_bus=0, **kwargs):
        """Initialize the PCA9685."""
        # Setup I2C interface for the device.
        self._device = None
        self._close_device = False
        if pi is None:
            pi = pigpio.pi()
        self._device = I2C(pi, i2c_bus, address)
        self.set_all_pwm_range(MAX_PWM)
        self.set_all(False)
        self._device.write_byte_data(MODE2, OUTDRV)
        self._device.write_byte_data(MODE1, ALLCALL)
        time.sleep(0.005)  # wait for oscillator
        mode1 = self._device.read_byte_data(MODE1)
        mode1 = mode1 & ~SLEEP  # wake up (reset sleep)
        self._device.write_byte_data(MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator

    def set_pwm_freq(self, freq_hz):
        """Set the PWM frequency to the provided value in hertz."""
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval = float(freq_hz)/prescaleval
        prescaleval -= 1.0
        logger.debug('Setting PWM frequency to {0} Hz'.format(freq_hz))
        logger.debug('Estimated pre-scale: {0}'.format(prescaleval))
        prescale = round(prescaleval)
        logger.debug('Final pre-scale: {0}'.format(prescale))
        oldmode = self._device.read_byte_data(MODE1);
        newmode = (oldmode & 0x7F) | 0x10    # sleep
        self._device.write_byte_data(MODE1, newmode)  # go to sleep
        self._device.write_byte_data(PRESCALE, prescale)
        self._device.write_byte_data(MODE1, oldmode)
        time.sleep(0.005)
        self._device.write_byte_data(MODE1, oldmode | 0x80)

    def set_pwm_range(self, channel, pwm_range):
        "Sets the maximum value of the PWM for the channel, all calls to set_pwm will be scaled"
        self.ranges[channel] = pwm_range

    def get_pwm_range(self, channel):
        return self.ranges[channel]

    def set_all_pwm_range(self, pwm_range):
        self.ranges = [pwm_range] * NUM_CHANNELS

    def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        if channel < 0 or channel >= NUM_CHANNELS:
            raise IndexError("Invalid channel {}".format(channel))
        on  = round(MAX_PWM * on  / self.ranges[channel])
        assert on <= MAX_PWM
        off = round(MAX_PWM * off / self.ranges[channel])
        assert off <= MAX_PWM
        self._device.write_byte_data(LED0_ON_L+4*channel, on & 0xFF)
        self._device.write_byte_data(LED0_ON_H+4*channel, on >> 8)
        self._device.write_byte_data(LED0_OFF_L+4*channel, off & 0xFF)
        self._device.write_byte_data(LED0_OFF_H+4*channel, off >> 8)

    def set_all_pwm(self, on, off):
        """Sets all PWM channels."""
        self._device.write_byte_data(ALL_LED_ON_L, on & 0xFF)
        self._device.write_byte_data(ALL_LED_ON_H, on >> 8)
        self._device.write_byte_data(ALL_LED_OFF_L, off & 0xFF)
        self._device.write_byte_data(ALL_LED_OFF_H, off >> 8)
    
    def set(self, channel, high):
        "Sets the pin to either 100% on or 100% off"
        if high:
            on  = FULL_ON_OFF
            off = 0
        else:
            on  = 0
            off = FULL_ON_OFF
        self._device.write_byte_data(LED0_ON_L+4*channel, on & 0xFF)
        self._device.write_byte_data(LED0_ON_H+4*channel, on >> 8)
        self._device.write_byte_data(LED0_OFF_L+4*channel, off & 0xFF)
        self._device.write_byte_data(LED0_OFF_H+4*channel, off >> 8)
        return high

    def set_all(self, high):
        if high:
            on  = FULL_ON_OFF
            off = 0
        else:
            on  = 0
            off = FULL_ON_OFF
        self._device.write_byte_data(ALL_LED_ON_L, on & 0xFF)
        self._device.write_byte_data(ALL_LED_ON_H, on >> 8)
        self._device.write_byte_data(ALL_LED_OFF_L, off & 0xFF)
        self._device.write_byte_data(ALL_LED_OFF_H, off >> 8)

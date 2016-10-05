#!/usr/bin/env python3
"""PCA9685 / pigpio unified interface"""
__author__ = "Daniel Casner <www.danielcasner.org>"

import pigpio
import PCA9685
import logging

logger = logging.getLogger(__name__)

class GpioNumException(Exception):
    pass

class PCA9685Pi(pigpio.pi):
    "Subclass for pigpio Pi interface with unified PCA9685 control"
    
    EXTENDER_OFFSET = 0x100
    EXTENDER_MASK   = 0xF00
    EXTENDER_SHIFT  = 8
    GPIO_MASK       = 0x0FF
    
    def __init__(self, i2c_bus=0, extender_addresses=[PCA9685.PCA9685_ADDRESS], *args, **kwargs):
        pigpio.pi.__init__(self, *args, **kwargs)
        self.extenders = [PCA9685.PCA9685(addr, self, i2c_bus) for addr in extender_addresses]
        for e in extenders:
            e.set_all_pwm_range(255) # Default to the same range as pigpio

    def _extendedGPIO(self, gpioNum):
        "Returns the extender index (or None) and gpio number"
        if gpioNum & self.EXTENDER_MASK == 0:
            return None, gpioNum
        else:
            extInd = (gpioNum >> self.EXTENDER_SHIFT) - 1
            if extInd > len(self.extenders):
                raise GpioNumException("No extender that high", gpioNum)
            elif (gpioNum & self.GPIO_MASK) >= PCM9685.NUM_CHANNELS:
                raise GpioNumException("Invalid gpio number", gpioNum)
            else:
                return self.extenders[extInd], gpioNum & self.GPIO_MASK

    def set_PWM_frequency(self, user_gpio, frequency):
        try:
            extender, gpioNum = self._extendedGPIO(user_gpio)
        except GpioNumException as e:
            logger.warn(str(e))
            return pigpio.PI_BAD_USER_GPIO
        else:
            if extender is None:
                return pigpio.pi.set_PWM_frequency(self, user_gpio, frequency)
            elif user_gpio & self.GPIO_MASK != 0:
                logger.error("Extender PWM frequency can only be set on base extender address")
                return pigpio.PI_BAD_USER_GPIO
            else:
                return extender.set_PWM_freq(frequency)
    
    def set_PWM_range(self, user_gpio, range):
        try:
            extender, gpioNum = self._extendedGPIO(user_gpio)
        except GpioNumException as e:
            logger.warn(str(e))
            return pigpio.PI_BAD_USER_GPIO
        else:
            if extender is None:
                return pigpio.pi.set_PWM_range(self, user_gpio, range)
            else:
                return extender.set_pwm_range(gpioNum, range)
    
    def set_PWM_dutycycle(self, user_gpio, dutycycle, delay=0):
        try:
            extender, gpioNum = self._extendedGPIO(user_gpio)
        except GpioNumException as e:
            logger.warn(str(e))
            return pigpio.PI_BAD_USER_GPIO
        else:
            if extender is None:
                return pigpio.pi.set_PWM_dutycycle(self, user_gpio, dutycycle)
            else:
                dutyRange = extender.get_pwm_range(gpioNum)
                if dutycycle > dutyRange
                    return pigpio.PI_BAD_DUTYCYCLE
                elif delay > dutyRange
                    return pigpio.PI_BAD_DUTYCYCLE
                else:
                    on  = delay
                    off = (dutycycle + delay) % dutyRange
                    return extender.set_pwm(gpioNum, on, off)

    def write(self, gpio, level):
        try:
            extender, gpioNum = self._extendedGPIO(user_gpio)
        except GpioNumException as e:
            logger.warn(str(e))
            return pigpio.PI_BAD_USER_GPIO
        else:
            if extender is None:
                return pigpio.pi.write(self, gpio, level)
            else:
                return extender.set(gpioNum, level)

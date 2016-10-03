from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(name              = 'Adafruit_PCA9685_pigpio',
      version           = '0.1.0',
      author            = 'Daniel Casner',
      author_email      = 'daniel@danielcasner.org',
      description       = 'Python code to use the PCA9685 PWM servo/LED controller with a Raspberry Pi or BeagleBone Black.',
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/DanielCasner/Adafruit_Python_PCA9685/',
      dependency_links  = ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.6.5'],
      install_requires  = ['pigpio'],
      packages          = find_packages())

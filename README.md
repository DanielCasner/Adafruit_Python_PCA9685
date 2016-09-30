# Adafruit Python PCA9685: PIGPIO Edition
Fork of the Adafruit Python PCA9685 PWM hat library altered to work with the pigpio daemon on the Raspberry Pi. There are three major changes

1. The I2C bus runs through the pigpio daemon
2. An API is available which is a subclass of the pigpio interface class and presents the PCA9685 outputs as additional channels on the pigpio output.
3. This implementation focuses on python3, python2.7 might work but is not explicitly supported

## Installation

To install the library from source (recommended) run the following commands on a Raspberry Pi or other Debian-based OS system:

    sudo apt-get install git build-essential python-dev
    cd ~
    git clone https://github.com/DanielCasner/Adafruit_Python_PCA9685.git
    cd Adafruit_Python_PCA9685
    sudo python setup.py install

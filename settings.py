import os

import board
from adafruit_blinka.board.beagleboard import beaglebone_black

# Standard Bela
SCL = board.SCL
SDA = board.SDA

if os.environ.get('PEPPER'):
  # I2C interface 1, used by Bela Pepper
  SCL = beaglebone_black.pin.I2C1_SCL
  SDA = beaglebone_black.pin.I2C1_SDA

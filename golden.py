# Turn off all the Neotrellis LEDs.

# portions
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2021-2022 org.yoyodyne

import os
import sys
import time

from adafruit_blinka.board.beagleboard import beaglebone_black
import adafruit_neotrellis.neotrellis
from board import SCL, SDA
import busio

COLOR1 = (80,50,30)
COLOR2 = (70,40,20)
COLOR3 = (60,30,10)
COLOR4 = (50,20,0)

if os.environ.get('PEPPER'):
    SCL = beaglebone_black.pin.I2C1_SCL
    SDA = beaglebone_black.pin.I2C1_SDA
i2c_bus = busio.I2C(SCL, SDA)

trellis = adafruit_neotrellis.neotrellis.NeoTrellis(i2c_bus)

for i in range(0,4):
    trellis.pixels[i] = COLOR4
for i in range(4,8):
    trellis.pixels[i] = COLOR4
for i in range(8,12):
    trellis.pixels[i] = COLOR4
for i in range(12,16):
    trellis.pixels[i] = COLOR4

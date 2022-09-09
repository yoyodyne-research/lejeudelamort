# Walk a light down the path of a raster image as quickly as possible.

# This sets all pixels individually in order to erase 15/16ths of them.
# The results do not feel 16 ms fast.

# portions
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2021-2022 org.yoyodyne

import os
import sys
import time

from adafruit_blinka.board.beagleboard import beaglebone_black
from adafruit_neotrellis.neotrellis import NeoTrellis
from board import SCL, SDA
import busio

COLOR0 = (0,0,0)
COLOR1 = (80,50,30)
COLOR2 = (70,40,20)
COLOR3 = (60,30,10)
COLOR4 = (50,20,0)

if os.environ.get('PEPPER'):
    SCL = beaglebone_black.pin.I2C1_SCL
    SDA = beaglebone_black.pin.I2C1_SDA
i2c_bus = busio.I2C(SCL, SDA)

trellis = NeoTrellis(i2c_bus)

i = 0
while True:
    for j in range(16):
        if j != i:
            trellis.pixels[j] = COLOR0
        else:
            trellis.pixels[i] = COLOR4
    i = (i + 1) % 16
    time.sleep(1)

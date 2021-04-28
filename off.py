# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# alterations 2021 org.yoyodyne
#
# Turn off all the Neotrellis LEDs.

import sys
import time

from adafruit_blinka.board.beagleboard import beaglebone_black
import adafruit_neotrellis.neotrellis
import board
import busio

sys.path.append('.')
import settings
sys.path.pop()

i2c_bus = busio.I2C(settings.SCL, settings.SDA)
trellis = adafruit_neotrellis.neotrellis.NeoTrellis(i2c_bus)
OFF = (0, 0, 0)
for i in range(16):
    trellis.pixels[i] = OFF
    # throttle a tad.
    time.sleep(0.05)

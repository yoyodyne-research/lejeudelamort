# Turn off all the Neotrellis LEDs.

# portions
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2021-2022 org.yoyodyne

import os
import sys
import time

import adafruit_neotrellis.neotrellis
from board import SCL, SDA
import busio

OFF = (0, 0, 0)

i2c_bus = busio.I2C(SCL, SDA)
trellis = adafruit_neotrellis.neotrellis.NeoTrellis(i2c_bus)
for i in range(16):
    trellis.pixels[i] = OFF
    # throttle a tad.
    time.sleep(0.05)

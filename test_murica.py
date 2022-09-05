""" Wave the freak flag for one second."""

import os
import time
import unittest

from adafruit_blinka.board.beagleboard import beaglebone_black
from adafruit_neotrellis.neotrellis import NeoTrellis
from board import SCL, SDA
import busio

r = (200, 0, 0)
w = (200, 200, 200)
b = (0, 0, 200)
image = [
    b, b, r, r,
    b, b, w, w,
    r, r, r, r,
    w, w, w, w
]

def raise_flag(trellis):
    for i in range(0, 16):
        trellis.pixels[i] = image[i]

def lower_flag(trellis):
    for i in range(0, 16):
        trellis.pixels[i] = (0,0,0)


class TestMurica(unittest.TestCase):
    def test_murica(self):
        if os.environ.get('PEPPER'):
            # switch to I2C interface 1, used by Bela Pepper
            SCL = beaglebone_black.pin.I2C1_SCL
            SDA = beaglebone_black.pin.I2C1_SDA
        i2c_bus = busio.I2C(SCL, SDA)
        trellis = NeoTrellis(i2c_bus)
        raise_flag(trellis)
        time.sleep(1)
        lower_flag(trellis)
        time.sleep(1)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

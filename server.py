# Receives OSC messages from this Bela at port 65001.
# Uses 0/1 on message /1/push{event} as button unlit/lit.

# Portions of code adapted from:
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# 2021-2022 org.yoyodyne Yoyodyne Research

import asyncio
import logging
import os
import re
import time

from adafruit_blinka.board.beagleboard import beaglebone_black
from adafruit_neotrellis.neotrellis import NeoTrellis
from board import SCL, SDA
import busio
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('server')


def grad(gamma:float):
    """ Intensity gradient from upper left to lower right.
        Gamma is tweaked so that it looks gradual. """
    for i in range(16):
        v = int(pow(i/16,gamma)*256)
        trellis.pixels[i] = (v,v,v)


def clear():
    """ set all pixels to black """
    for i in range(16):
        trellis.pixels[i] = color_clear


def button_event_receiver(event):
    """ respond to OSC message /1/push{event}
        by lighting up button {event} where
        event is a number from 1 to 16 """
    # this will be called when button events are received
    address = "/1/push{}".format(event.number+1)
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = color_press
        logger.debug('sending 1 to {}'.format(address))
        client.send_message(address, 1)
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = color_clear
        logger.debug('sending 0 to {}'.format(address))
        client.send_message(address, 0)


def default_handler(addr, val):
    if not enabled:
        return
    scale = 256   # 8-bit max intensity
    gamma = 2.0  # gamma-ish
    i = int(re.match('/1/push(\d+)', addr).groups()[0]) - 1
    j = int(pow(val, gamma) * scale);
    trellis.pixels[i] = (j,j,j)


async def loop():
    while True:
        # call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 milliseconds or so
        await asyncio.sleep(0.1)


async def init_main():
    server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()


if os.environ.get('PEPPER'):
  # switch to I2C interface 1, used by Bela Pepper
  SCL = beaglebone_black.pin.I2C1_SCL
  SDA = beaglebone_black.pin.I2C1_SDA

ip = '0.0.0.0'        # localhost
port = os.environ.get('OSC_PORT') or 65001

color_press = (200,200,200)
color_clear = (0,0,0)
gamma = 2.0

# create the trellis
client = udp_client.SimpleUDPClient(ip, port)
sleeptime = 0.01
enabled = True

i2c_bus = busio.I2C(SCL, SDA)
trellis = NeoTrellis(i2c_bus)

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

logging.info('starting server')
logging.info('listening on {}:{}'.format(ip, port))
logging.info('drawing gamma gradient 1.0')
grad(1.0)
time.sleep(2)
logging.info('drawing gamma gradient 2.0')
grad(2.0)
time.sleep(2)
logging.info('drawing gamma gradient 3.0')
grad(3.0)
time.sleep(2)
clear()
logging.info('done drawing gamma gradients')

logging.info('waiting for events')
logging.info('press Ctrl-C to quit')

asyncio.run(init_main())

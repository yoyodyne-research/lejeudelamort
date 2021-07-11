# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# alterations 2021 org.yoyodyne

# Send to and receive from Bela project 'osc'.
# Match IP addrs with bela and use neotrellis template.

import asyncio
import re
import sys
import time

from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_blinka.board.beagleboard import beaglebone_black
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import murica

sys.path.append('.')
import settings
sys.path.pop()

#ip = "192.168.1.65"  # nori

#ip = "192.168.1.71"  # bela
#port = 65002

ip = "0.0.0.0"        # localhost
port = 65001
gamma = 2.0

# create the trellis
client = udp_client.SimpleUDPClient(ip, port)
sleeptime = 0.01
enabled = True


def salute():
    murica.raise_flag(trellis)
    time.sleep(1)
    murica.lower_flag(trellis)
    time.sleep(1)


def grad(gamma=gamma):
    for i in range(16):
        v = int(pow(i / 16, gamma) * 256);
        trellis.pixels[i] = (v, v, v);


def button_event_receiver(event):
    # this will be called when button events are received
    address = "/1/push{}".format(event.number+1)
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = (200,200,200)
        print('sending 1 to {}'.format(address))
        client.send_message(address, 1)
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = (0,0,0)
        print('sending 0 to {}'.format(address))
        client.send_message(address, 0)


def default_handler(addr, r, g, b):
    if not enabled:
        return
    rmax = 256
    i = int(re.match('/1/push(\d+)', addr).groups()[0]) - 1
    c = (int(pow(r, gamma) * rmax), int(pow(g, gamma) * rmax), int(pow(b, gamma) * rmax))
    trellis.pixels[i] = c


async def loop():
    while True:
        # call the sync function call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 milliseconds or so
        await asyncio.sleep(0.1)


async def init_main():
    server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    await loop()  # Enter main loop of program
    transport.close()  # Clean up serve endpoint


i2c_bus = busio.I2C(settings.SCL, settings.SDA)
trellis = NeoTrellis(i2c_bus)

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)

#salute()
grad(1.0)
time.sleep(2)
grad(2.0)
time.sleep(2)
grad(3.0)
time.sleep(2)
asyncio.run(init_main())


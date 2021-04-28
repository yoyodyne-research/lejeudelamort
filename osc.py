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

sys.path.append('.')
import settings
sys.path.pop()

#ip = "192.168.1.65"  # nori
ip = "192.168.1.71"  # bela
port = 65002
client = udp_client.SimpleUDPClient(ip, port)
sleeptime = 0.01
enabled = True

i2c_bus = busio.I2C(settings.SCL, settings.SDA)

# create the trellis
trellis = NeoTrellis(i2c_bus)

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
palette = [OFF, BLUE, CYAN]

# this will be called when button events are received
def blink(event):
    address = "/1/push{}".format(event.number+1)
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = GREEN
        print('sending 1 to {}'.format(address))
        client.send_message(address, 1)
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = OFF
        print('sending 0 to {}'.format(address))
        client.send_message(address, 0)


def default_handler(addr, args):
    if not enabled:
        return
    #print('received {} destined for {}'.format(args, addr))
    i = int(re.match('/1/push(\d+)', addr).groups()[0]) - 1
    trellis.pixels[i] = palette[args]


for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    trellis.pixels[i] = PURPLE
    time.sleep(0.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(0.05)

dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(default_handler)


async def loop():
    while True:
        # call the sync function call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 milliseconds or so
        await asyncio.sleep(0.01)


async def init_main():
    server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    print(transport, protocol)

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


ip = "0.0.0.0"
port = 65001

asyncio.run(init_main())


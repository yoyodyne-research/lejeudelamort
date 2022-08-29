An OSC server that drives an Adafruit Neotrellis.

This guy is specially wired to work with

https://github.com/yoyodyne-research/gameofdeath

You need Python 3.7 or later for the Bela to get the correct `asyncio`.
Say you put that Python 3.9 at /opt/python3.9 .

    /opt/python/bin/python3.9 -m venv venv
    . venv/bin/activate
    pip3 install -r requirements.txt

then you're ready to

    python3 scripts/server.py

when in the venv or

    ./server

when you are not in the venv.


## Inspecting I2C

```
i2cdetect -y -r 1
i2cdetect -y -r 2
```

and look for an entry at 2e.


![Bruce](etc/legod.jpg)


An OSC server that drives an Adafruit Neotrellis.

This guy is specially wired to work with

https://github.com/yoyodyne-research/gameofdeath

You need Python 3.7 or later for the Bela to get the correct `asyncio`.
Say you put that Python at /opt/python .

    virtualenv -p /opt/python/bin/python3 venv
    . venv/bin/activate
    pip3 install -r requirements.txt

then you're ready to

    python3 scripts/server.py

or

    ./server


## Inspecting I2C
```
i2cdetect -y -r 1
i2cdetect -y -r 2
```

![Bruce](etc/legod.jpg)

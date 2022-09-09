# lejeudelamort

An OSC server that drives an Adafruit Neotrellis.

This guy is specially wired to work with

https://github.com/yoyodyne-research/gameofdeath

## Setup

You need Python 3.7 or later for the Bela to get the correct `asyncio`.
Say you put Python 3.9 at `/opt/python3.9` .

    /opt/python/bin/python3.9 -m venv venv
    . venv/bin/activate
    pip3 install -r requirements.txt

If you are on PEPPER,

    export PEPPER=1

then you're ready to

    python3 scripts/run-server.py

The neotrellis will light up a grad 3 times at varying gamma and then go black wating for OSC messages of the form `/1/push<n>`, where n is the button number.

## Debugging

To check your Bela can actually see the Neotrellis,

```
i2cdetect -y -r 1
i2cdetect -y -r 2
```

and look for an entry at `2e`.

## systemd

Assumption: you cloned to /root/lejeudelamort.

    cp lejeudelamort.service /etc/systemd/system
    systemctl daemon reload
    systemctl start lejeudelamort
    systemctl status lejeudelamort


![Bruce](etc/legod.jpg)

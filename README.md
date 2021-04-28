This guy is specially wired to work with

https://github.com/yoyodyne-research/gameofdeath

You need a Python 3.7 build for the Bela to get the correct `asyncio`.

    virtualenv -p /opt/python3.7/python3 venv
    . venv/bin/activate
    python osc.py

## Inspecting I2C

   i2cdetect -y -r 1
   i2cdetect -y -r 2

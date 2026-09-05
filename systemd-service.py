#!/usr/bin/env bash
# target for service definition to run.
# * it expects $HOME/lejeudelamort
# * it expects $HOME/venv

source /root/.venv/rpi/bin/activate
python3 /root/lejeudelamort/server.py


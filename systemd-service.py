#!/usr/bin/env bash
# target for service definition to run.
# * it expects $HOME/lejeudelamort
# * it expects $HOME/venv

# if you need to:
#export PEPPER=1

source /root/venv/bin/activate
python3 /root/lejeudelamort/server.py


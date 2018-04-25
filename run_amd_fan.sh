#!/bin/sh

# Stop
/usr/bin/killall amd_fan.py

# Start
/usr/bin/nohup amd_fan.py &

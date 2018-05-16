#!/bin/sh

app_dir="amd_fan"
app_name="amd_fan.py"


# Stop
/usr/bin/killall ${app_name}

# Start
cd $HOME/bin/${app_dir}
/bin/rm -f ./nohup.out
./${app_name} &

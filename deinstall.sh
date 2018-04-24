#!/bin/sh

config_dir=".amd_fan"
config_file="amd_fan_config.py"
app_dir="amd_fan"
app_name="amd_fan.py"


# Delete link to application file
echo "Delete link to application file: '/opt/ethos/bin/$app_name'"
/bin/rm /opt/ethos/bin/$app_name

# Delete application
echo "Delete application in: '$HOME/bin/$app_dir'"
/bin/rm -f $HOME/bin/$app_dir/*
/bin/rmdir /$HOME/bin/$app_dir



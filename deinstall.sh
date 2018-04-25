#!/bin/sh

app_dir="amd_fan"
app_name="amd_fan.py"
run_app_script="run_amd_fan.sh"
stop_app_script="stop_amd_fan.sh"


# Delete link to application file
echo "Delete links to application files"
/bin/rm /opt/ethos/bin/${run_app_script}
/bin/rm /opt/ethos/bin/${stop_app_script}


# Delete application
echo "Delete application in: '$HOME/bin/$app_dir'"
/bin/rm -f $HOME/bin/${app_dir}/*
/bin/rmdir /$HOME/bin/${app_dir}

#!/bin/sh

config_file="amd_fan_config.py"
app_dir="amd_fan"
app_name="amd_fan.py"
run_app_script="run_amd_fan.sh"
stop_app_script="stop_amd_fan.sh"

# Create directory for application
if ! [ -d "$HOME/bin/$app_dir" ]
then
    echo "The directory '$HOME/bin/$app_dir' not found. Create it."
    mkdir $HOME/bin/${app_dir}
else
    echo "The directory '$HOME/bin/$app_dir' already exists".
fi


# To place a application file
if [ -f "$HOME/bin/$app_dir/$app_name" ]
then
    echo "Application file '$HOME/bin/$app_dir/$app_name' already exists. Backup it."
    mv $HOME/bin/${app_dir}/${app_name} $HOME/bin/${app_dir}/${app_name}.backup
fi
echo "Copying application files to '$HOME/bin/$app_dir/' directory"
/bin/cp ./__init__.py $HOME/bin/${app_dir}/__init__.py
/bin/cp ./${app_name} $HOME/bin/${app_dir}/${app_name}
/bin/cp ./${run_app_script} $HOME/bin/${app_dir}/${run_app_script}
/bin/cp ./${stop_app_script} $HOME/bin/${app_dir}/${stop_app_script}


# To place a configuration file
if [ -f "$HOME/bin/$app_dir/$config_file" ]
then
    echo "Configuration file '$HOME/bin/$app_dir/$config_file' already exists."
else
    echo "Copying configuration file '$config_file' to '$HOME/bin/$app_dir/' directory"
    /bin/cp ./${config_file} $HOME/bin/${app_dir}/${config_file}
fi


# Make link to application file
/bin/ln -fsv $HOME/bin/$app_dir/$run_app_script /opt/ethos/bin/$run_app_script
/bin/ln -fsv $HOME/bin/$app_dir/$stop_app_script /opt/ethos/bin/$stop_app_script


# Make the auto run








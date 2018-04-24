#!/bin/sh

config_dir=".amd_fan"
config_file="amd_fan_config.py"
app_dir="amd_fan"
app_name="amd_fan.py"


# Create directory for configuration file
if ! [ -d "$HOME/$config_dir" ]
then
    echo "The directory '$HOME/$config_dir' not found. Create it."
    mkdir $HOME/$config_dir
else
    echo "The directory '$HOME/$config_dir' already exists".
fi


# To place a configuration file
if [ -f "$HOME/$config_dir/$config_file" ]
then
    echo "Configuration file '$HOME/$config_dir/$config_file' already exists."
else
    echo "Copying configuration file '$HOME/$config_dir/$config_file' to '$config_dir' dyrectory"
    /bin/cp ./$config_file $HOME/$config_dir/$config_file
fi


# Create dyrectory for application
if ! [ -d "$HOME/bin/$app_dir" ]
then
    echo "The directory '$HOME/bin/$app_dir' not found. Create it."
    mkdir $HOME/bin/$app_dir
else
    echo "The directory '$HOME/bin/$app_dir' already exists".
fi


# To place a application file
if [ -f "$HOME/bin/$app_dir/$app_name" ]
then
    echo "Application file '$HOME/bin/$app_dir/$app_name' already exists. Backup it."
    mv $HOME/bin/$app_dir/$app_name $HOME/bin/$app_dir/$app_name.backup
    echo "Copying application file '$app_name' to '$HOME/bin/$app_dir/' dyrectory"
    /bin/cp ./$app_name $HOME/bin/$app_dir/$app_name
else
    echo "Copying application file '$app_name' to '$HOME/bin/$app_dir/' dyrectory"
    /bin/cp ./$app_name $HOME/bin/$app_dir/$app_name
fi


# Make link to application file
ln -fsv $HOME/bin/$app_dir/$app_name /opt/ethos/bin/$app_name


# Make the autorun








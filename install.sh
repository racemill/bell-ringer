#!/bin/bash

BELLRINGER_PATH="/usr/local/bell-ringer"
SYSTEMD_PATH="/etc/systemd/system"

BELLRINGER_SERVICE_FILE="bell-ringer.service"

sudo mkdir -p $BELLRINGER_PATH
sudo cp *.py $BELLRINGER_PATH
sudo cp index.html $BELLRINGER_PATH

sudo cp $BELLRINGER_SERVICE_FILE $SYSTEMD_PATH

sudo systemctl enable $BELLRINGER_SERVICE_FILE
sudo systemctl start $BELLRINGER_SERVICE_FILE

# Overwrites everything else in system crontab...
sudo cp crontab.txt /etc/crontab

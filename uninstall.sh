#!/bin/sh

sudo systemctl disable keepalive
sudo systemctl stop keepalive
rm /etc/systemd/system/keepalive.service
sudo systemctl daemon-reload

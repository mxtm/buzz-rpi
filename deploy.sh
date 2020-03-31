#!/bin/bash

# TODO: write a deployment script that goes from a fresh RPi Raspbian install to Buzz unit
# This should go similar to as follows:

# create directory /home/pi/motion

# install motion from Github releases

# copy /etc/default/motion into place

# copy /etc/motion/motion.conf into place

# install frp from Github releases (binary zip for arm), copy to /usr/bin

# copy systemd services into place

# reload systemd daemon

# copy /etc/frp/frpc.ini into place

# install python3 libraries face_recognition and firebase_admin (globally)

# fix permissions

# restart motion systemd service

# enable motion systemd service

# enable frpc systemd service

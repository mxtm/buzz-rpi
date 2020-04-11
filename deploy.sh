#!/bin/bash

# TODO: write a deployment script that goes from a fresh RPi Raspbian install to Buzz unit
# This should go similar to as follows:

# create directories /home/pi/motion and /home/pi/motion/logs

# install motion from Github releases

# copy /etc/default/motion into place

# copy /etc/motion/motion.conf into place

# install frp from Github releases (binary zip for arm), copy to /usr/bin

# copy systemd services into place

# reload systemd daemon

# copy /etc/frp/frpc.ini into place

# install python3 libraries face_recognition and firebase_admin (globally)

# install opencv-python version 4.1.0.25 (latest doesn't work on rpi) with deps (see: https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/)

# fix permissions

# restart motion systemd service

# enable motion systemd service

# enable frpc systemd service

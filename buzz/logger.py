#!/usr/bin/env python3

from datetime import datetime

SERVER_LOG = "/home/pi/buzz-rpi/logs/server.log"
CLIENT_LOG = "/home/pi/buzz-rpi/logs/client.log"

def log(msg, client=False):
    destination = CLIENT_LOG if client else SERVER_LOG
    formatted_msg = datetime.now().strftime("%m/%d/%Y %H:%M:%S - ") + msg
    print(formatted_msg)
    with open(destination, "a") as file:
        file.write(formatted_msg + "\n")

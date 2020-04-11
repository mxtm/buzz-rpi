#!/usr/bin/env python3

from datetime import datetime
from multiprocessing.connection import Client

def log(msg):
    formatted_msg = datetime.now().strftime("%m/%d/%Y %H:%M:%S - ") + msg
    print(formatted_msg)
    with open("/home/pi/buzz-rpi/logs/client.log", "a") as file:
        file.write(formatted_msg + "\n")

with Client("/home/pi/buzz-rpi/buzz_socket", "AF_UNIX") as conn:
    log("Sent event_start to server")
    conn.send("event_start")

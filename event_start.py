#!/usr/bin/env python3

from multiprocessing.connection import Client

with Client("/home/pi/buzz-rpi/buzz_socket", "AF_UNIX") as conn:
    conn.send("event_start")

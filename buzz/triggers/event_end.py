#!/usr/bin/env python3

from multiprocessing.connection import Client

import yaml

from buzz.logger import log

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    CONFIG = yaml.load(config_file)

def main():
    with Client(CONFIG["core"]["socket"], "AF_UNIX") as conn:
        conn.send("event_end")
        log("Sent event_end to server", client=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from buzz.logger import log

import yaml
from multiprocessing.connection import Client

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    config = yaml.load(config_file)

def main():
    with Client(config["core"]["socket"], "AF_UNIX") as conn:
        conn.send("event_start")
        log("Sent event_start to server", client=True)

if __name__ == "__main__":
    main()

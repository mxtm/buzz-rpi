#!/usr/bin/env python3

from datetime import datetime

import yaml

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)

def log(msg, client=False):
    destination = CONFIG["logs"]["client"] if client else CONFIG["logs"]["server"]
    formatted_msg = datetime.now().strftime("%m/%d/%Y %H:%M:%S - ") + msg
    print(formatted_msg)
    with open(destination, "a") as file:
        file.write(formatted_msg + "\n")

#!/usr/bin/env python3

import yaml
from datetime import datetime

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

def log(msg, client=False):
    destination = config["logs"]["client"] if client else config["logs"]["server"]
    formatted_msg = datetime.now().strftime("%m/%d/%Y %H:%M:%S - ") + msg
    print(formatted_msg)
    with open(destination, "a") as file:
        file.write(formatted_msg + "\n")

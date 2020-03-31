#!/usr/bin/env python3

from datetime import datetime

with open("/home/pi/buzz-rpi/logs/motion.log", "a") as file:
    file.write(f"Motion event ended at {str(datetime.now())}\n")

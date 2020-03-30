#!/usr/bin/env python3
from datetime import datetime
with open("/home/pi/buzz-rpi/motion.log", "a") as file:
    file.write(f"Motion event started at {str(datetime.now())}\n")

#!/usr/bin/env python3

import firebase_admin
from firebase_admin import messaging, credentials
from datetime import datetime

cred = credentials.Certificate('/home/pi/buzz-rpi/firebase_admin_key.json')
default_app = firebase_admin.initialize_app(cred)
topic = 'global'

with open("/home/pi/buzz-rpi/motion.log", "a") as file:
    file.write(f"Motion event started at {str(datetime.now())}\n")

message = messaging.Message(
            notification = messaging.Notification(
                title='Buzz',
                body='Bzz. Bzz. Motion was detected at your door.'
            ),
            topic=topic
)

response = messaging.send(message)

with open("/home/pi/buzz-rpi/motion.log", "a") as file:
    file.write(f"Message {response} sent\n")

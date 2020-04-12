#!/usr/bin/env python3

import firebase_admin
from firebase_admin import messaging, credentials

FIREBASE_CREDENTIAL_CERTIFICATE = "/home/pi/buzz-rpi/firebase_admin_key.json"

class FirebaseConnector:
    def send_notification(self, notification_body):
        message = messaging.Message(
            notification = messaging.Notification(
                title="Buzz",
                body=notification_body,
            ),
            topic="global",
        )

        return messaging.send(message)

    def __init__(self):
        cred = credentials.Certificate(FIREBASE_CREDENTIAL_CERTIFICATE)
        default_app = firebase_admin.initialize_app(cred)

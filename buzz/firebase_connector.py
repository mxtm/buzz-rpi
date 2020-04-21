#!/usr/bin/env python3

from buzz.logger import log

import firebase_admin
import os
import requests
import yaml
from firebase_admin import messaging, credentials, firestore, storage
from PIL import Image
from PIL.ExifTags import TAGS

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

class FirebaseConnector:
    def upload_to_storage(self, source_file):
        destination_name = os.path.basename(source_file)

        blob = self.bucket.blob(destination_name)
        with open(source_file, "rb") as file:
            blob.upload_from_file(file)

    def send_notification(self, notification_body):
        message = messaging.Message(
            notification = messaging.Notification(
                title="Buzz",
                body=notification_body,
            ),
            topic="global",
        )

        return messaging.send(message)

    def get_visitor_info(self):
        visitors_ref = self.db.collection(u'visitors')
        docs = visitors_ref.stream()

        visitors = {}

        for doc in docs:
            visitors[doc.id] = doc.to_dict()

        return visitors

    def get_visitor_photos(self, visitors_info):
        for k, v in visitors_info.items():
            image = requests.get(v['image'], allow_redirects=True)
            open(config["visitors"]["photos_target"] + k + ".jpg", "wb").write(image.content)
            log(f"Downloaded photo for visitor {k}")

        for image in os.listdir(config["visitors"]["photos_target"]):
            image_path = config["visitors"]["photos_target"] + image
            image_object = Image.open(image_path)

            try:
                for k, v in image_object._getexif().items():
                    if TAGS.get(k) == "Orientation":
                        orientation = v
                
                if orientation == 3:
                    image_object = image_object.rotate(180)
                elif orientation == 6:
                    image_object = image_object.rotate(270)
                elif orientation == 8:
                    image_object = image_object.rotate(90)
            except AttributeError:
                pass

            image_object.save(image_path)

    def __init__(self):
        cred = credentials.Certificate(config["firebase"]["credential_certificate"])
        default_app = firebase_admin.initialize_app(cred,
                                                    {
                                                        'storageBucket': config["firebase"]["storage_bucket"]
                                                    })

        self.db = firestore.client()
        self.bucket = storage.bucket()

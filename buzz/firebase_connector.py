#!/usr/bin/env python3

import os
from datetime import datetime

from firebase_admin import messaging, credentials, firestore, storage
import requests
import yaml
from PIL import Image
from PIL.ExifTags import TAGS
import firebase_admin

from buzz.logger import log


with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)

class FirebaseConnector:

    def add_visitor_log_entry(self, visitors):
        timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        data = {
            u"timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
            u"video": u"",
            u"visitors": visitors
        }
        self.visitors_log_ref.document(u"{0}".format(timestamp.encode('utf-8'))).set(data)

    def upload_to_storage(self, source_file):
        destination_name = os.path.basename(source_file)

        blob = self.bucket.blob(destination_name)
        with open(source_file, "rb") as file:
            blob.upload_from_file(file)
            blob.make_public()

        query = self.visitors_log_ref.where(u"video",
                                            u"==",
                                            u"").order_by(
                                                u"timestamp",
                                                direction=firestore.Query.DESCENDING).limit(1)
        docs = query.stream()

        for doc in docs:
            self.visitors_log_ref.document(doc.id).set({u"video": blob.public_url}, merge=True)

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
        visitors_ref = self.database.collection(u'visitors')
        docs = visitors_ref.stream()

        visitors = {}

        for doc in docs:
            visitors[doc.id] = doc.to_dict()

        return visitors

    def get_visitor_photos(self, visitors_info):
        for key, value in visitors_info.items():
            image = requests.get(value['image'], allow_redirects=True)
            open(CONFIG["visitors"]["photos_target"] + key + ".jpg", "wb").write(image.content)
            log(f"Downloaded photo for visitor {key}")

        for image in os.listdir(CONFIG["visitors"]["photos_target"]):
            image_path = CONFIG["visitors"]["photos_target"] + image
            image_object = Image.open(image_path)

            try:
                for key, value in image_object._getexif().items():
                    if TAGS.get(key) == "Orientation":
                        orientation = value

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
        cred = credentials.Certificate(CONFIG["firebase"]["credential_certificate"])
        default_app = firebase_admin.initialize_app(cred,
                                                    {
                                                        'storageBucket':
                                                        CONFIG["firebase"]["storage_bucket"]
                                                    })

        self.database = firestore.client()
        self.bucket = storage.bucket()

        self.visitors_log_ref = self.database.collection(u'visitors_log')

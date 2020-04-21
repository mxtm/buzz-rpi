#!/usr/bin/env python3

import face_recognition
import yaml

from buzz.logger import log

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)

def process_visitor_images(visitor_info):
    known_face_encodings = []
    known_face_names = []

    for key, value in visitor_info.items():
        image = face_recognition.load_image_file(
            CONFIG["visitors"]["photos_target"] + key + ".jpg")
        face_encoding = face_recognition.face_encodings(image, num_jitters=100)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(value['firstName'] + " " + value['lastName'])
        log(f"Visitor {key} processed and ready")

    return (known_face_encodings, known_face_names)

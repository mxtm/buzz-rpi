#!/usr/bin/env python3

from buzz.logger import log

import face_recognition
import yaml

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

def process_visitor_images(visitor_info):
    known_face_encodings = []
    known_face_names = []
    
    for k, v in visitor_info.items():
        image = face_recognition.load_image_file(config["visitors"]["photos_target"] + k + ".jpg")
        face_encoding = face_recognition.face_encodings(image, num_jitters=100)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(v['firstName'] + " " + v['lastName'])
        log(f"Visitor {k} processed and ready")

    return (known_face_encodings, known_face_names)

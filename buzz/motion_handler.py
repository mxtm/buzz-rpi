#!/usr/bin/env python3

from buzz.logger import log

import cv2
import face_recognition
import numpy as np
import yaml
from datetime import datetime

with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

def handle_motion(firebase_connector, known_face_encodings, known_face_names):

    log("Motion event started")

    video_capture = cv2.VideoCapture(config["core"]["video_capture_url"])
    log("Ready to grab frames")

    notification_response = firebase_connector.send_notification("Bzz. Bzz. Motion was detected at your door.")
    log(f"Notification {notification_response} sent")

    face_locations = []
    face_encodings = []
    face_names = []

    for i in range(0, 46):
        log(f"Checking frame {i} for faces")

        ret, frame = video_capture.read()

        if config["super-debug"]["copy_attempted_face_detection_frames"]:
            cv2.imwrite(config["super-debug"]["attempts_destination"] + datetime.now().strftime("%m-%d-%Y_%H_%M_%S_") + str(i) + ".jpg", frame)

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)#, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,
                                                         face_locations)

        if len(face_encodings) != 0:
            log(f"Face detected in frame {i}")
            notification_response = firebase_connector.send_notification("I see someone at your door! Checking if I know them...")
            log(f"Notification {notification_response} sent")
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings,
                                                        face_encoding)
                name = "An unknown visitor"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                log(f"Known face names: {str(known_face_names)}")
                log(f"Face distances: {str(face_distances)}")
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    firebase_connector.add_visitor_log_entry(name)
                                
                    notification_response = firebase_connector.send_notification(name + " is at your door!")
                    log(f"Notification {notification_response} sent")

            break

    video_capture.release()
    log("Destroyed frame capture object")

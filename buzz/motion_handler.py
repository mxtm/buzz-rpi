#!/usr/bin/env python3

from buzz.logger import log

import cv2
import face_recognition

def handle_motion(firebase_connector, video_capture):
    log("Motion event started")

    notification_response = firebase_connector.send_notification("Bzz. Bzz. Motion was detected at your door.")
    log(f"Notification {notification_response} sent")

    face_locations = []
    face_encodings = []
    face_names = []

    for i in range(0, 51):
        log(f"Checking frame {i} for faces")

        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)

        if len(face_locations) != 0:
            log(f"Face found in frame {i}")

            notification_response = firebase_connector.send_notification("A face was detected at your door!")
            log(f"Notification {notification_response} sent")

            break

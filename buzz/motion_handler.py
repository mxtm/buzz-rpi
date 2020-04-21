#!/usr/bin/env python3

from buzz.logger import log

import cv2
import face_recognition
import numpy as np

def handle_motion(firebase_connector, video_capture, known_face_encodings,
                  known_face_names):

    log("Motion event started")

    notification_response = firebase_connector.send_notification("Bzz. Bzz. Motion was detected at your door.")
    log(f"Notification {notification_response} sent")

    face_locations = []
    face_encodings = []
    face_names = []

    for i in range(0, 46):
        log(f"Checking frame {i} for faces")

        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)#, number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,
                                                         face_locations)

        if len(face_encodings) != 0:
            log(f"Face detected in frame {i}")
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
                                
                    notification_response = firebase_connector.send_notification(name + " is at your door!")
                    log(f"Notification {notification_response} sent")

            break

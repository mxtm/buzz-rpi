#!/usr/bin/env python3

import cv2
import face_recognition
import firebase_admin
import numpy as np
from datetime import datetime
from firebase_admin import messaging, credentials
from multiprocessing.connection import Listener

def log(msg):
    formatted_msg = datetime.now().strftime("%m/%d/%Y %H:%M:%S - ") + msg
    print(formatted_msg)
    with open("/home/pi/buzz-rpi/logs/server.log", "a") as file:
        file.write(formatted_msg + "\n")

def prepare_firebase_connection():
    cred = credentials.Certificate("/home/pi/buzz-rpi/firebase_admin_key.json")
    default_app = firebase_admin.initialize_app(cred)

def send_notification(notification_body):
    message = messaging.Message(
            notification = messaging.Notification(
                title="Buzz",
                body=notification_body,
            ),
            topic="global",
    )

    return messaging.send(message)

if __name__ == "__main__":

    prepare_firebase_connection()
    log("Ready to connect to Firebase")

    video_capture = cv2.VideoCapture('http://127.0.0.1:8081')
    log("Ready to grab frames")

    while True:
        with Listener("/home/pi/buzz-rpi/buzz_socket", "AF_UNIX") as listener:
            log("Ready to accept connections")
            with listener.accept() as conn:
                if conn.recv() == "event_start":
                    log("Motion event started")
                    notification_response = send_notification("Bzz. Bzz. Motion was detected at your door.")
                    log(f"Notification {notification_response} sent")
                    face_locations = []
                    face_encodings = []
                    face_names = []
                    for i in range(0, 51):
                        log(f"Checking frame {i} for faces")
                        ret, frame = video_capture.read()
                        cv2.imwrite(f"/home/pi/buzz-rpi/motion/{i}-{str(datetime.now())}.jpg", frame)
                        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_small_frame = small_frame[:, :, ::-1]
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        if len(face_locations) != 0:
                            log(f"Face found in frame {i}")
                            notification_response = send_notification("A face was detected at your door!")
                            log(f"Notification {notification_response} sent")
                            break

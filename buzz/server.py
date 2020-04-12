#!/usr/bin/env python3

from buzz.firebase_connector import FirebaseConnector
from buzz.logger import log
from buzz.motion_handler import handle_motion

import cv2
from multiprocessing.connection import Listener

DEBUG = True
SOCKET = "/tmp/buzz_socket"

def main():
    firebase_connector = FirebaseConnector()
    log("Firebase connection ready")

    video_capture = cv2.VideoCapture('http://127.0.0.1:8081')
    log("Ready to grab frames")

    while True:
        with Listener(SOCKET, "AF_UNIX") as listener:
            log("Ready to accept connections")
            with listener.accept() as conn:
                received_signal = conn.recv()
                if received_signal == "event_start":
                    handle_motion(firebase_connector, video_capture)
                elif received_signal == "event_end" and DEBUG:
                    notification_response = firebase_connector.send_notification("DEBUG: Motion event ended.")
                    log(f"Notification {notification_response} sent")

if __name__ == "__main__":
    main()

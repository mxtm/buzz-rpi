#!/usr/bin/env python3

import os
import pickle
from multiprocessing.connection import Listener

import yaml

from buzz.firebase_connector import FirebaseConnector
from buzz.logger import log
from buzz.motion_handler import handle_motion
from buzz.utility import process_visitor_images


with open("/home/pi/buzz-rpi/buzz/config.yml", "r") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)

def main():
    firebase_connector = FirebaseConnector()
    log("Firebase connection ready")

    visitor_info = firebase_connector.get_visitor_info()
    log("Got visitor info")

    if not CONFIG["super-debug"]["dont_redownload_visitor_photos"]:
        firebase_connector.get_visitor_photos(visitor_info)
        log("Finished getting visitor photos")
    else:
        log("Skipping getting visitor photos per config")

    if not CONFIG["super-debug"]["dont_reprocess_visitor_faces"]:
        known_face_encodings, known_face_names = process_visitor_images(visitor_info)
    else:
        log("Attempting to skip processing visitor faces per config")
        try:
            visitor_faces_pickle = open(
                CONFIG["super-debug"]["visitor_faces_pickle"],
                'rb'
            )
            saved_face_data = pickle.load(visitor_faces_pickle)
            known_face_encodings, known_face_names = saved_face_data
            log("Loaded saved visitor face data")
        except FileNotFoundError:
            log("Failed to load visitor face data, generating and saving it")
            known_face_encodings, known_face_names = process_visitor_images(visitor_info)
            visitor_faces_pickle = open(
                CONFIG["super-debug"]["visitor_faces_pickle"],
                'wb'
            )
            face_data = (known_face_encodings, known_face_names)
            pickle.dump(face_data, visitor_faces_pickle)

    try:
        os.unlink('/tmp/buzz_socket')
    except FileNotFoundError:
        pass

    while True:
        with Listener(CONFIG["core"]["socket"], "AF_UNIX") as listener:
            log("Ready to accept connections")
            with listener.accept() as conn:
                received_signal = conn.recv()

                if CONFIG["core"]["debug"]:
                    log(f"Received signal: {received_signal}")

                if received_signal == "event_start":
                    handle_motion(firebase_connector, known_face_encodings, known_face_names)
                elif received_signal == "event_end" and CONFIG["core"]["debug"]:
                    notification_response = firebase_connector.send_notification(
                        "DEBUG: Motion event ended.")
                    log(f"Notification {notification_response} sent")
                elif "movie_end" in received_signal:
                    log(f"Video file ended {received_signal.split(' ')[1]}")
                    firebase_connector.upload_to_storage(received_signal.split(' ')[1])
                    log(f"Uploaded video file to Firebase Storage")

if __name__ == "__main__":
    main()

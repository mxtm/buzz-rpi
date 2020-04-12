#!/usr/bin/env python3

from buzz.logger import log

from multiprocessing.connection import Client

SOCKET = "/tmp/buzz_socket"

def main():
    with Client(SOCKET, "AF_UNIX") as conn:
        conn.send("event_start")
        log("Sent event_start to server", client=True)

if __name__ == "__main__":
    main()

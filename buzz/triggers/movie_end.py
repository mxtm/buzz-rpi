#!/usr/bin/env python3

from buzz.logger import log

import sys
from multiprocessing.connection import Client

SOCKET = "/tmp/buzz_socket"

def main():
    video_file = sys.argv[1]

    with Client(SOCKET, "AF_UNIX") as conn:
        conn.send("movie_end " + video_file)
        log("Sent movie_end " + video_file + " to server", client=True)

if __name__ == "__main__":
    main()

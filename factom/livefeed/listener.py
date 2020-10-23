import logging
import socket
import struct
from typing import Callable


class LiveFeedListener:
    """
    A simple class that listens to Factomd LiveFeed and performs a custom handle
    function on each event sent over the feed.

    Args:
        handle (callable): A function receiving a bytes-like variable as its
            only parameter. Handles all LiveFeed events.
        host (str): The host of the LiveFeed to listen to.
        port (int): The port on which LiveFeed is configured.
    """
    def __init__(self, handle: Callable, host: str = "127.0.0.1", port: int = 8040):
        self.handle = handle
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            logging.debug("Listening for LiveFeed connection...")
            conn, address = s.accept()
            with conn:
                logging.debug(f"Connected to LiveFeedAPI: {address}")
                while True:
                    protocol_version = conn.recv(1)
                    if not protocol_version:
                        break
                    conn.sendall(protocol_version)
                    if protocol_version[0] == 1:
                        next_message_size_bytes = conn.recv(4)
                        next_message_size = struct.unpack("<i", next_message_size_bytes)[0]
                        if next_message_size is not None:
                            message_data = conn.recv(next_message_size)
                            remaining_bytes = next_message_size - len(message_data)
                            while remaining_bytes > 0:
                                message_data += conn.recv(remaining_bytes)
                                remaining_bytes = next_message_size - len(message_data)
                            self.handle(message_data)

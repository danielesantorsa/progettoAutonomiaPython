import socket
import time

class UDPsender:
    def __init__(self, port=12346):
        self.port = port
        self.running = True

    def broadcast_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = b"BATTLESHIP_SERVER"
            while self.running:
                s.sendto(message, ('<broadcast>', self.port))
                print("Inviato messaggio di discovery UDP")
                time.sleep(3)
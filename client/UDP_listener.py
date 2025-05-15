# client/udp_listener.py
import socket

class UDPListener:
    def __init__(self, port=12346):
        self.port = port

    def discover_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(("", self.port))
            s.settimeout(10)
            try:
                data, addr = s.recvfrom(1024)
                if data == b"BATTLESHIP_SERVER":
                    return addr[0]
            except socket.timeout:
                return None

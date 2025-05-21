import socket
import psutil
import threading
from time import sleep

class UDPSender:
    def __init__(self, tcp_port=5000, udp_port=6000, interval=5):
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.interval = interval

    def start_broadcast(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        message = f"{self.tcp_port}".encode("utf-8")

        while True:
            try:
                for interface, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                            if addr.broadcast:  # <--- FIX qui
                                udp_socket.sendto(message, (addr.broadcast, self.udp_port))
            except Exception as e:
                print(f"[UDP] Errore durante il broadcast: {e}")

            sleep(self.interval)

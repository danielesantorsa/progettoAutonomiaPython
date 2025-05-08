import socket
import psutil
from time import sleep
    # Funzione per inviare volantini UDP in broadcast
    # Funzione per inviare volantini UDP in broadcast
def start_udp_broadcast(server_port, client_udp_port=5001):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = f"{server_port}"

        while True:
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                        try:
                            udp_socket.sendto(message.encode("utf-8"), (addr.broadcast, client_udp_port))
                            print(f"[UDP] Volantino inviato a {addr.broadcast}:{client_udp_port}")
                        except Exception as e:
                            print(f"[UDP] Errore su {addr.broadcast}: {e}")
            sleep(5)

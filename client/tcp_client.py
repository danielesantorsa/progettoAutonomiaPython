import socket

class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None

    def connetti(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))
        print(f"Connesso al server TCP su {self.server_ip}:{self.server_port}")

    def invia_mossa(self, x, y):
        messaggio = f"{x},{y}"
        self.sock.sendall(messaggio.encode())

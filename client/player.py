import socket
import json
import threading
from shared.protocol import send_json, recv_json

class PlayerClient:
    def init(self, server_ip, server_port, udp_port):
        self.server_addr = (server_ip, server_port)
        self.udp_port = udp_port
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.bind(('0.0.0.0', self.udp_port))
        self.udp_thread = None
        self.running = True
        self.player_id = None

def connect(self):
    self.tcp_sock.connect(self.server_addr)
    print(f"[CLIENT] Connesso al server {self.server_addr}")
    welcome = recv_json(self.tcp_sock)
    if welcome and welcome.get("type") == "welcome":
        self.player_id = welcome["player"]
        print(f"[CLIENT] Benvenuto, sei il giocatore {self.player_id}")
    else:
        raise Exception("Errore nella connessione iniziale")

def send_move(self, row, col):
    move = {
        "type": "move",
        "row": row,
        "col": col
    }
    send_json(self.tcp_sock, move)

def receive_update(self):
    return recv_json(self.tcp_sock)

def start_udp_listener(self, callback=None):
    def listen():
        while self.running:
            try:
                data, _ = self.udp_sock.recvfrom(1024)
                message = data.decode('utf-8')
                print(f"[UDP] Notifica ricevuta: {message}")
                if callback:
                    callback(message)
            except:
                break

    self.udp_thread = threading.Thread(target=listen, daemon=True)
    self.udp_thread.start()

def close(self):
    self.running = False
    self.udp_sock.close()
    self.tcp_sock.close()

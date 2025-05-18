# client/tcp_client.py
import socket
import threading

class TCPClient:
    def __init__(self, server_ip, server_port=12345):
        self.server_address = (server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gui = None

    def set_gui(self, gui):
        self.gui = gui

    def connect_and_listen(self):
        self.sock.connect(self.server_address)
        print("Connesso al server.")
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Ricevuto: {message}")
                if self.gui:
                    self.gui.handle_server_message(message)
            except Exception as e:
                print(f"Errore: {e}")
                break

    def send_move(self, x, y):
        move = f"MOVE {x} {y}"
        self.sock.sendall(move.encode())

    def close(self):
        try:
            self.sock.sendall(b"QUIT")
        except:
            pass
        self.sock.close()

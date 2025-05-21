import socket
import threading
from game import Game

class TCPServer:
    def __init__(self, game: Game, host='0.0.0.0', port=5000):
        self.game = game
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"[TCP] In ascolto su {self.host}:{self.port}...")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"[TCP] Connessione ricevuta da {addr}")

            if not self.game.add_player(conn, addr):
                conn.sendall(b"SERVER PIENO\n")
                conn.close()
                continue

            player_index = len(self.game.players) - 1
            client_thread = threading.Thread(target=self.handle_client, args=(conn, player_index), daemon=True)
            client_thread.start()

    def handle_client(self, conn, player_index):
        self.game.wait_for_ready()
        conn.sendall(b"INIZIO\n")

        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                move = data.decode().strip()
                result = self.game.process_move(player_index, move)
                conn.sendall(result.encode() + b"\n")
        except ConnectionError:
            print(f"[TCP] Disconnessione del giocatore {player_index}")
        finally:
            conn.close()
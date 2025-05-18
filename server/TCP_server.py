# server/tcp_server.py
import socket
import threading
from game import GameManager

class TCPServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.game_manager = GameManager()
        self.clients = []
        self.lock = threading.Lock()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server in ascolto su {self.host}:{self.port}")

            while True:
                client_conn, client_addr = server_socket.accept()
                with self.lock:
                    if len(self.clients) >= 2:
                        print(f"Connessione da {client_addr} rifiutata (server pieno)")
                        client_conn.sendall(b"SERVER_FULL")
                        client_conn.close()
                        continue

                    self.clients.append(client_conn)
                    print(f"Giocatore connesso da {client_addr}")
                    self.game_manager.add_player(client_conn)
                    threading.Thread(target=self.handle_client, args=(client_conn,), daemon=True).start()

    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                self.game_manager.process_message(conn, data)
        except Exception as e:
            print(f"Errore client: {e}")
        finally:
            with self.lock:
                if conn in self.clients:
                    self.clients.remove(conn)
            self.game_manager.remove_player(conn)
            conn.close()

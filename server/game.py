import threading
from game import Gamemanager

class GameManager:
    def __init__(self):
        self.players = {}    
        self.turn = None
        self.lock = threading.Lock()

    def add_player(self, conn):
        with self.lock:
            player_id = len(self.players) + 1
            self.players[conn] = player_id
            print(f"Giocatore {player_id} aggiunto")
            if len(self.players) == 2:
                self.start_game()

    def start_game(self):
        print("Entrambi i giocatori connessi. Inizio partita!")
        for conn, pid in self.players.items():
            msg = f"START {pid}".encode()
            conn.sendall(msg)
        self.turn = 1  # Inizia il player 1

    def process_message(self, conn, message):
        with self.lock:
            player_id = self.players.get(conn)
            if player_id != self.turn:
                conn.sendall(b"NOT_YOUR_TURN")
                return

            # Riceviamo una mossa: es "MOVE 3 5"
            decoded = message.decode()
            if decoded.startswith("MOVE"):
                print(f"Player {player_id} ha inviato: {decoded}")
                for other_conn in self.players.keys():
                    if other_conn != conn:
                        other_conn.sendall(message)

                # Passa il turno
                self.turn = 2 if self.turn == 1 else 1

            elif decoded == "QUIT":
                self.remove_player(conn)

    def remove_player(self, conn):
        with self.lock:
            if conn in self.players:
                player_id = self.players[conn]
                print(f"Player {player_id} disconnesso")
                del self.players[conn]
                for other_conn in self.players.keys():
                    other_conn.sendall(b"OTHER_PLAYER_LEFT")
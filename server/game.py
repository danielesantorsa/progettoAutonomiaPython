import threading

class Game:
    def __init__(self):
        self.players = []  # Lista delle socket dei giocatori
        self.lock = threading.Lock()
        self.ready_event = threading.Event()
        self.turn = 0
        self.board_state = [{}, {}]  # Stato semplificato per esempio

    def add_player(self, conn, addr):
        with self.lock:
            if len(self.players) >= 2:
                return False  # Troppi giocatori
            self.players.append((conn, addr))
            print(f"[GAME] Giocatore aggiunto: {addr}")
            if len(self.players) == 2:
                print("[GAME] Entrambi i giocatori connessi. Inizio partita.")
                self.ready_event.set()  # Segnala inizio gioco
            return True

    def wait_for_ready(self):
        self.ready_event.wait()  # Blocco finché non ci sono 2 giocatori

    def get_opponent_index(self, player_index):
        return 1 - player_index

    def process_move(self, player_index, data):
        with self.lock:
            if player_index != self.turn:
                return "WAIT"

            # Esempio semplice: si memorizza una mossa (tipo "B4")
            self.board_state[player_index][data] = True
            self.turn = self.get_opponent_index(player_index)
            return "OK"

    def get_status(self):
        with self.lock:
            return {
                'turn': self.turn,
                'players': len(self.players)
            }

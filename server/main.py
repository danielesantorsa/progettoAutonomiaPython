import socket
import threading
from .state import GlobalState
from .UDP_sender import send_UDP_notification
from shared.protocol import recv_json, send_json
from .game import GameState

class GameServer:
    def __init__(self, host="0.0.0.0", port = 5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.global_state = GlobalState()
        self.lock = threading.Lock()
        
    def Start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"Server in ascolto su: {self.host}:{self.port}")

        for player_id in range(2):
            # Aspetta che un client si connetta
            conn, addr = self.server_socket.accept()
            print(f"Giocatore {player_id} connesso da {addr}")

            # Aggiunge il giocatore alla lista globale
            self.global_state.add_player(conn, addr) 

            # Manda un messaggio di benvenuto al client con l'ID del giocatore
            send_json(conn, {"type": "welcome", "player":player_id})

            
            
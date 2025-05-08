import socket
import threading
# Scopo: importa la classe GlobalState che gestisce lo 
# stato condiviso del gioco (come la lista dei giocatori connessi, i turni, ecc.).
from .state import GlobalState
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
            # Crea un nuovo thread per gestire la comunicazione con il client
            thread = threading.Thread(
                # La funzione che gestisce la comunicazione
                target = self.clientHandler,
                # Passa la connessione, l'indirizzo e l'ID del giocatore
                args = (conn, addr, player_id),
                # Imposta il thread come "daemon", in modo che si chiuda quando il programma principale termina
                daemon = True
            )
        
        # Avvia il thred
        thread.start()

        # Quando entrambi i client sono connessi, avvio lo stato del gioco
        self.global_state.game_state = GameState()
        print("Partita inizializzata.")

    def clientHandler(self, conn, addr, player_id):
        try:
            while True:
                # Riceve i dati in formato JSON dal client
                data = recv_json(conn)
                if not data:
                    print(f"Giocatore {player_id} si è disconnesso.")
                    break

                # Sezione protetta da mutex per gestire la mossa in modo sicuro
                with self.lock:
                    # Calcola il risultato della mossa
                    result = self.global_state.game_state.process_move(player_id, data)

                    # Risposta al giocatore che ha fatto la mossa
                    send_json(conn, result["to_player"])

                    # Risposta all’avversario
                    opponent_conn = self.global_state.get_opponent_conn(player_id)
                    if opponent_conn:
                        send_json(opponent_conn, result["to_opponent"])

        except Exception as e:
            print(f"Errore nel thread del Giocatore {player_id}: {e}")
        finally:
            conn.close()
            
            
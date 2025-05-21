# Importa il modulo threading, necessario per gestire più client contemporaneamente in modo sicuro
import threading

# Classe che rappresenta la logica centrale del gioco (es. Battaglia Navale)
class Game:
    def __init__(self):
        # Lista di tuple (connessione socket, indirizzo) dei giocatori connessi
        self.players = []

        # Lock (mutua esclusione) per proteggere l’accesso concorrente a variabili condivise
        self.lock = threading.Lock()

        # Evento utilizzato per sincronizzare l’inizio del gioco (si attiva solo quando ci sono 2 giocatori)
        self.ready_event = threading.Event()

        # Indice del giocatore che ha il turno attivo (0 o 1)
        self.turn = 0

        # Stato semplificato del campo di gioco per entrambi i giocatori
        # Ogni elemento è un dizionario delle mosse effettuate
        self.board_state = [{}, {}]

    # Metodo per aggiungere un nuovo giocatore alla partita
    def add_player(self, conn, addr):
        with self.lock:  # Sezione protetta: solo un thread alla volta può accedervi
            if len(self.players) >= 2:
                return False  # Se ci sono già 2 giocatori, si rifiuta il nuovo

            # Aggiunge il giocatore alla lista
            self.players.append((conn, addr))
            print(f"[GAME] Giocatore aggiunto: {addr}")

            # Se sono connessi 2 giocatori, si segnala l’inizio del gioco
            if len(self.players) == 2:
                print("[GAME] Entrambi i giocatori connessi. Inizio partita.")
                self.ready_event.set()  # Sblocca tutti i thread in attesa dell’inizio
            return True  # Giocatore accettato con successo

    # Metodo che blocca il thread finché non sono connessi 2 giocatori
    def wait_for_ready(self):
        self.ready_event.wait()  # Attesa bloccante finché l’evento non viene attivato

    # Metodo per ottenere l’indice dell’avversario (serve per alternare i turni)
    def get_opponent_index(self, player_index):
        return 1 - player_index  # Se sei il player 0 → ritorna 1, se sei il 1 → ritorna 0

    # Metodo per gestire una mossa effettuata da un giocatore
    def process_move(self, player_index, data):
        with self.lock:  # Protezione concorrente
            if player_index != self.turn:
                return "WAIT"  # Non è il turno del giocatore, deve aspettare

            # Registra la mossa effettuata dal giocatore (es. posizione “B4”)
            self.board_state[player_index][data] = True

            # Cambia turno all’altro giocatore
            self.turn = self.get_opponent_index(player_index)

            return "OK"  # Mossa accettata e registrata

    # Metodo per ottenere lo stato attuale del gioco (numero giocatori connessi e di chi è il turno)
    def get_status(self):
        with self.lock:
            return {
                'turn': self.turn,               # Indica a chi tocca giocare
                'players': len(self.players)    # Indica quanti giocatori sono connessi
            }

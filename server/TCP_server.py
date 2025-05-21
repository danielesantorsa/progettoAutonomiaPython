# Importa il modulo socket per creare comunicazioni TCP tra server e client
import socket

# Importa il modulo threading per gestire più client contemporaneamente con thread separati
import threading

# Importa la classe Game che contiene la logica e lo stato del gioco
from game import Game

# Classe che implementa il server TCP per il gioco
class TCPServer:
    # Costruttore della classe. Inizializza il server TCP.
    def __init__(self, game: Game, host='0.0.0.0', port=5000):
        self.game = game  # Oggetto Game condiviso tra i client per gestire partita e turni
        self.host = host  # Indirizzo IP su cui il server è in ascolto (0.0.0.0 = tutte le interfacce)
        self.port = port  # Porta TCP su cui il server accetta le connessioni
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea il socket TCP
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permette il riutilizzo rapido della porta

    # Metodo che avvia il server TCP e accetta connessioni dai client
    def start_server(self):
        self.server_socket.bind((self.host, self.port))  # Collega il socket all’indirizzo e alla porta specificati
        self.server_socket.listen(2)  # Il server può mettere in coda al massimo 2 richieste di connessione
        print(f"[TCP] In ascolto su {self.host}:{self.port}...")  # Messaggio di log

        while True:
            # Accetta una nuova connessione (bloccante finché un client si connette)
            conn, addr = self.server_socket.accept()
            print(f"[TCP] Connessione ricevuta da {addr}")  # Log della connessione

            # Tenta di aggiungere il giocatore alla partita
            if not self.game.add_player(conn, addr):
                # Se ci sono già 2 giocatori, rifiuta la connessione
                conn.sendall(b"SERVER PIENO\n")
                conn.close()
                continue  # Torna ad aspettare altri client

            # Calcola l’indice del giocatore (0 o 1) in base alla posizione nella lista dei giocatori
            player_index = len(self.game.players) - 1

            # Crea un thread per gestire la comunicazione con questo client
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(conn, player_index),
                daemon=True  # Il thread termina automaticamente alla chiusura del programma
            )
            client_thread.start()  # Avvia il thread per gestire il client

    # Metodo che gestisce la comunicazione con un singolo client
    def handle_client(self, conn, player_index):
        self.game.wait_for_ready()  # Aspetta che entrambi i giocatori siano connessi

        # Invia al client un messaggio per segnalare l’inizio del gioco
        conn.sendall(b"INIZIO\n")

        try:
            while True:
                data = conn.recv(1024)  # Riceve i dati inviati dal client (massimo 1024 byte)
                if not data:
                    break  # Se non riceve nulla, la connessione è chiusa

                move = data.decode().strip()  # Decodifica e pulisce il messaggio ricevuto
                result = self.game.process_move(player_index, move)  # Processa la mossa con la logica del gioco

                conn.sendall(result.encode() + b"\n")  # Invia al client il risultato della mossa
        except ConnectionError:
            # Se il client si disconnette o c'è un errore nella comunicazione
            print(f"[TCP] Disconnessione del giocatore {player_index}")
        finally:
            conn.close()  # Chiude la connessione in ogni caso (fine partita o errore)

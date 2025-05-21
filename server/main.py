# Importa il modulo threading che permette di eseguire più operazioni in parallelo (multithreading)
import threading

# Importa la classe TCPServer dal file TCP_server.py, che gestisce le connessioni dei client via TCP
from TCP_server import TCPServer

# Importa la classe UDPSender dal file UDP_sender.py, che invia pacchetti broadcast via UDP per annunciare il server nella rete
from UDP_sender import UDPSender

# Importa la classe Game dal file game.py, che contiene tutta la logica e lo stato della partita
from game import Game

# Funzione principale che viene eseguita quando il server viene avviato
def main():
    print("[SERVER] Avvio del server...")  # Stampa un messaggio di avvio nel terminale per informare l'utente

    # Crea un'istanza dell'oggetto Game, che gestirà i giocatori, i turni, le mosse e sincronizzerà l'accesso ai dati condivisi
    game = Game()

    # Crea un oggetto UDPSender, che invierà messaggi di broadcast UDP per far conoscere il server ai client nella rete locale
    udp_sender = UDPSender()

    # Crea un thread (processo leggero) separato che esegue la funzione start_broadcast() dell'oggetto udp_sender
    # Il parametro daemon=True indica che il thread si chiuderà automaticamente quando il programma principale termina
    udp_thread = threading.Thread(target=udp_sender.start_broadcast, daemon=True)

    # Avvia il thread UDP per iniziare a inviare messaggi di broadcast in rete ogni pochi secondi
    udp_thread.start()

    # Stampa un messaggio di conferma che il broadcast UDP è stato avviato con successo
    print("[UDP] Broadcast avviato.")

    # Crea un oggetto TCPServer, passando come parametro l’oggetto game, così che i client connessi possano accedere alla partita
    tcp_server = TCPServer(game)

    # Crea un thread separato che eseguirà la funzione start_server() dell’oggetto TCPServer per accettare connessioni TCP dai client
    tcp_thread = threading.Thread(target=tcp_server.start_server, daemon=True)

    # Avvia il thread TCP, permettendo al server di iniziare ad accettare connessioni da client sulla porta specificata
    tcp_thread.start()

    # Stampa un messaggio che indica che il server è in ascolto e pronto ad accettare giocatori
    print("[TCP] Server in ascolto.")

    # Ciclo infinito che mantiene il programma attivo.
    # Può essere esteso in futuro per accettare comandi da terminale (es. per amministrare il server)
    try:
        while True:
            pass  # In questo punto si potrebbe inserire un menu per l'amministratore o controlli sullo stato del server
    except KeyboardInterrupt:
        # Se l'utente preme CTRL+C nel terminale, il server stampa un messaggio e termina in modo pulito
        print("\n[SERVER] Arresto manuale ricevuto.")

# Controlla che il file venga eseguito direttamente (e non importato come modulo da un altro file)
# Se è così, esegue la funzione main()
if __name__ == '__main__':
    main()

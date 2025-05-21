import threading
from TCP_server import TCPServer
from UDP_sender import UDPSender
from game import Game


def main():
    print("[SERVER] Avvio del server...")

    # Inizializzazione stato del gioco
    game = Game()

    # Avvio UDP broadcast (volantinaggio IP)
    udp_sender = UDPSender()
    udp_thread = threading.Thread(target=udp_sender.start_broadcast, daemon=True)
    udp_thread.start()
    print("[UDP] Broadcast avviato.")

    # Avvio server TCP per ricevere connessioni
    tcp_server = TCPServer(game)
    tcp_thread = threading.Thread(target=tcp_server.start_server, daemon=True)
    tcp_thread.start()
    print("[TCP] Server in ascolto.")

    # Main loop di controllo (bloccante, ma può essere esteso per comandi da console)
    try:
        while True:
            pass  # Qui si potrebbero aggiungere comandi admin
    except KeyboardInterrupt:
        print("\n[SERVER] Arresto manuale ricevuto.")


if __name__ == '__main__':
    main()

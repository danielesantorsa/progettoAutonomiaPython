# Importa il modulo socket per la comunicazione in rete (UDP in questo caso)
import socket

# Importa la libreria psutil per ottenere informazioni sulle interfacce di rete (come IP e broadcast)
import psutil

# Importa threading nel caso si voglia eseguire il broadcast in un thread separato
import threading

# Importa sleep per inserire pause tra i messaggi broadcast
from time import sleep

# Classe che si occupa di inviare messaggi UDP in broadcast per annunciare la presenza del server
class UDPSender:
    # Costruttore della classe: inizializza porta TCP da annunciare, porta UDP su cui mandare il messaggio e intervallo di invio
    def __init__(self, tcp_port=5000, udp_port=6000, interval=5):
        self.tcp_port = tcp_port        # Porta TCP del server da comunicare ai client
        self.udp_port = udp_port        # Porta UDP su cui inviare i messaggi broadcast
        self.interval = interval        # Tempo (in secondi) tra un broadcast e l'altro

    # Metodo che avvia il volantinaggio UDP (broadcast) in modo ciclico
    def start_broadcast(self):
        # Crea un socket UDP
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Abilita la modalità broadcast sul socket
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Prepara il messaggio da inviare: la porta TCP del server, codificata in byte
        message = f"{self.tcp_port}".encode("utf-8")

        # Ciclo infinito che invia il broadcast ogni tot secondi
        while True:
            try:
                # Per ogni interfaccia di rete disponibile nel sistema
                for interface, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        # Considera solo gli indirizzi IPv4 non di loopback (127.0.0.1)
                        if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                            # Controlla se l'interfaccia ha un indirizzo broadcast
                            if addr.broadcast:
                                # Invia il messaggio alla rete in broadcast sulla porta UDP specificata
                                udp_socket.sendto(message, (addr.broadcast, self.udp_port))
            except Exception as e:
                # Se c'è un errore (es. un'interfaccia senza broadcast), stampa il messaggio ma continua
                print(f"[UDP] Errore durante il broadcast: {e}")

            # Attende il numero di secondi indicato prima di inviare il prossimo broadcast
            sleep(self.interval)

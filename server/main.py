# Importo le librerie 
import socket
import threading

# Inserisco un numero massimo di giocatori per partita
MAX_PLAYERS = 2

# Permetto che i messaggi possano essere codificati e decodificati in UTF-8
def encode_message(msg: str) -> bytes:
    return msg.encode('utf-8')
    

def decode_message(data: bytes) -> str:
    return data.decode('utf-8').strip()

# Creo la classe 
class ServerBattagliaNavale:
    def __init__(self, host = '127.0.0.1', port = 9999):

        # Configuro indirizzo IP e porta del server
        self.host = host
        self.port = port

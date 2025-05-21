import socket

class UDPListener:
    def __init__(self, porta=5000):
        self.porta = porta

    def attendi_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.porta))
        print("In attesa del server UDP broadcast...")

        dati, addr = sock.recvfrom(1024)
        messaggio = dati.decode()
        print(f"Ricevuto messaggio UDP: {messaggio} da {addr}")

        ip, porta = messaggio.split(":")
        return ip, int(porta)

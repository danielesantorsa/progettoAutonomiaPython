from game_interface import InterfacciaDiGioco
from UDP_listener import UDPListener
from tcp_client import TCPClient

def main():
    # 1. Ascolta il messaggio broadcast del server
    udp = UDPListener()
    server_ip, server_port = udp.attendi_server()

    # 2. Connessione TCP al server
    tcp = TCPClient(server_ip, server_port)
    tcp.connetti()

    # 3. Avvia il gioco (puoi collegare TCPClient più avanti)
    gioco = InterfacciaDiGioco()
    gioco.run()

if __name__ == "__main__":
    main()

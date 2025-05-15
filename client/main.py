# client/main.py
import threading
from UDP_listener import UDPListener
from tcp_client import TCPClient
from game_interface import GameInterface

def main():
    udp_listener = UDPListener(port=12346)
    server_ip = udp_listener.discover_server()
    if not server_ip:
        print("Nessun server trovato.")
        return

    print(f"Server trovato: {server_ip}")

    client = TCPClient(server_ip=server_ip, server_port=12345)
    game_interface = GameInterface(client)

    client_thread = threading.Thread(target=client.connect_and_listen, daemon=True)
    client_thread.start()

    game_interface.run()

if __name__ == "__main__":
    main()

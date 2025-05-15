# server/main.py
import threading
from TCP_server import TCPServer
from UDP_sender import UDPsender

def main():
    udp_discovery = UDPsender(port=12346)
    udp_thread = threading.Thread(target=udp_discovery.broadcast_ip, daemon=True)
    udp_thread.start()

    server = TCPServer(host='0.0.0.0', port=12345)
    server.start_server()

if __name__ == "__main__":
    main()
            
import socket
import threading
from shared.protocol import encode_message, decode_message

class BattleshipClient:
    def init(self,server_ip='127.0.0.1',server_port='9999',):
        self.server_ip = server_ip
        self.server_port= server_port
        self.client_socket=socket.socket(socket.AD_INET,socket.SOCK_STREAM)
        
                    
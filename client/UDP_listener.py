import socket
import threading

class UDPListener:
def init(self, udp_port, callback=None):
self.udp_port = udp_port
self.callback = callback
self.running = True
self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
self.udp_sock.bind(('0.0.0.0', self.udp_port))
self.thread = threading.Thread(target=self.listen, daemon=True)

def start(self):
    self.thread.start()

def listen(self):
    while self.running:
        try:
            data, _ = self.udp_sock.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"[UDP] Notifica ricevuta: {message}")
            if self.callback:
                self.callback(message)
        except:
            break

def stop(self):
    self.running = False
    self.udp_sock.close()

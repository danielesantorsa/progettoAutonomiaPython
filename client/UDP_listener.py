# client/udp_listener.py
import socket

<<<<<<< HEAD
class UDPListener:
    def __init__(self, port=12346):
        self.port = port

    def discover_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(("", self.port))
            s.settimeout(10)
            try:
                data, addr = s.recvfrom(1024)
                if data == b"BATTLESHIP_SERVER":
                    return addr[0]
            except socket.timeout:
                return None
=======
#metodo costruttore
def __init__(self,host,port): #definisce l'indirizzo e la porta del server da cui riceverà i messaggi
    self.host=host
    self.port = port
    self.running = True
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)# crea il socket
    self.socket.bind((self.host,self.port))#lega il socket alla porta e al host specificati,progranna ascolta su quella porta i messaggi in arrivo via udp

def star_listening(self):
    #thread di ascolto per le notifiche udp
    listening_thread = threading.THREAD(target=self.listen_for_notifications)#thread che esegue listen_for_notifications
    listening_thread.daemon = True #il thread termina quando il thread principale termina
    listening_thread.start()#avvia il thread di ascolto

def listen_for_notifications(self):
    pass
>>>>>>> 82674f6 (commit)

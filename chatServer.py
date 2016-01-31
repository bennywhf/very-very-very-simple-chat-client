import socket
import threading

#################################################################
##############Very Very Very Simple Chat Client##################
#################################################################

class chatServerSide(threading.Thread):
    def __init__(self,address,socket,client_dict):
        self.address = address
        self.socket = socket
        self.clients = client_dict
        self.running = True
        threading.Thread.__init__(self)

    def run(self):
        while(self.running):
            try:
                data = self.socket.recv(1024)#hard written but could be argument for object.
                for connection in self.clients:
                    if(connection != self.address):
                        try:
                            self.clients[connection].send(data)
                        except socket.error as e:
                            #this socket is no longer open.
                            pass
            except Exception as e:
                print(e)
                self.running = False



            
class Server(threading.Thread):
    def __init__(self,port):
        self.serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.serversocket.bind(('localhost',port))
        self.serversocket.listen(5)
        self.running = True
        self.connections = {}
        threading.Thread.__init__(self)

    def run(self):
        while(self.running):
            print('waiting for client')
            (sock,address) = self.serversocket.accept()
            print('got connection')
            self.connections[address] = sock
            client = chatServerSide(address,sock,self.connections)
            client.start()

    def stop(self):
        self.running = False
        self.serversocket.close()
        


def main():
    s = Server(8914)
    s.start()
    try:
        while(True):
            pass
    except KeyboardInterrupt:
        s.stop()
main()

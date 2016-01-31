import socket
import threading
import select
class chatClientSide(threading.Thread):
    def __init__(self,address,port):
        self.sock = self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address,port))
        threading.Thread.__init__(self)
        self.running = True

    def send(self,msg):
        # for now only send the first 1024 bytes
        self.sock.send(msg[:1024])


    def run(self):
        while(self.running):
            if(select.select([self.sock],[],[])[0]):
                data = self.sock.recv(1024)
                print(data)

    def stop(self):
        self.running = False
        self.sock.shutdown(1)


def main():
    print('yo')
    client = chatClientSide('localhost',8914)
    client.start()
    user = raw_input('Please Enter a nickname (other users will see this name):')
    print('Hi '+user+', you may enter text and press the [Enter] key. All other users will receive the text.')
    try:
        while(True):
            d = raw_input()
            client.send(user+': '+d)
    except KeyboardInterrupt:
        print('closing')
        client.stop()
main()

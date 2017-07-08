import json
import socket
import threading
import time

__author__ = 'matsfunk'


class OOCSI:
    
    def __init__(self, handle, host='localhost', port=4444, callback=None):
        self.receivers = {handle: callback}
        self.reconnect = True
        self.connected = False
        
        # Connect the socket to the port where the server is listening
        self.server_address = (host, port)
        self.handle = handle
        print('connecting to %s port %s' % self.server_address)
        
        # start the connection thread        
        self.runtime = OOCSIThread(self)
        self.runtime.start()
        
        # block till we are connected
        while not self.connected:
            {}
        
    def init(self):
        try:
            # Create a TCP/IP socket        
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(self.server_address)
            
            try:
                # Send data
                message = self.handle + '(JSON)'
                self.internalSend(message)
            
                data = self.sock.recv(1024)
                if data.startswith('{'):  
                    print('connection established for ' + message)
                    # re-subscribe for channels
                    for channelName in self.receivers:
                        self.internalSend('subscribe {0}'.format(channelName))
                    self.connected = True
    
                while self.connected:
                    self.loop()
    
            finally:
                {}
        
        except: 
            {}
        
        
    def internalSend(self, msg):
        self.sock.sendall(msg + '\n')

    def loop(self):
        try:
            data = self.sock.recv(10 * 1024)
    
            if len(data) == 0:
                self.sock.close()
                self.connected = False
            if data.startswith('ping'):
                self.internalSend('.')
            if data.startswith('{'):
                self.receive(json.loads(data))
        except :
            {}


    def receive(self, event):
        sender = event['sender']
        recipient = event['recipient']
        
        # clean up the event
        del event['recipient']
        del event['sender']
        del event['timestamp']
        del event['data']
        
        if recipient in self.receivers and self.receivers[recipient] != None:
            self.receivers[recipient](sender, recipient, event)
#         else:
#             print('not good -------------- ', filteredEvent)

    def send(self, channelName, data):
        self.internalSend('sendraw {0} {1}'.format(channelName, json.dumps(data)))

    def subscribe(self, channelName, f):
        self.receivers[channelName] = f
        self.internalSend('subscribe {0}'.format(channelName))
    
    def unsubscribe(self, channelName):
        del self.receivers[channelName]
        self.internalSend('unsubscribe {0}'.format(channelName))

    def stop(self):
        self.reconnect = False
        self.internalSend('quit')
        self.sock.close()
        self.connected = False

    def handleEvent(self, sender, receiver, message):
        {}

class OOCSIThread(threading.Thread):

    def __init__(self, parent=None):
        self.parent = parent
        super(OOCSIThread, self).__init__()

    def run(self):
        while self.parent.reconnect:
            self.parent.init()
            if self.parent.reconnect:
                print('re-connecting to OOCSI')
                time.sleep(5)

        print('closing connection to OOCSI')

    def __stop(self):
        self.parent.stop()
        return threading.Thread.__stop(self) 

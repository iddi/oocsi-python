# Copyright (c) 2017 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

import json
import socket
import threading
import time
import uuid

__author__ = 'matsfunk'


class OOCSI:
    
    def __init__(self, handle=None, host='localhost', port=4444, callback=None):
        if handle == None or len(handle.strip()) == 0:
            self.handle = "OOCSIClient_" + uuid.uuid4().__str__().replace('-', '')[0:15];
        else:
            self.handle = handle
            
        self.receivers = {self.handle: [callback]}
        self.calls = {}
        self.services = {}
        self.reconnect = True
        self.connected = False
        
        # Connect the socket to the port where the server is listening
        self.server_address = (host, port)
        self.log('connecting to %s port %s' % self.server_address)
        
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
            
                data = self.sock.recv(1024).decode()
                if data.startswith('{'):  
                    self.log('connection established')
                    # re-subscribe for channels
                    for channelName in self.receivers:
                        self.internalSend('subscribe {0}'.format(channelName))
                    self.connected = True
                else:
                    if data.startswith('error'):
                        self.log(data)
                        self.reconnect = False
    
                while self.connected:
                    self.loop()
        
            finally:
                {}
        
        except: 
            {}
    
    def log(self, message):
        print('[{0}]: {1}'.format(self.handle, message))
        
    def internalSend(self, msg):
        try:
            self.sock.sendall((msg + '\n').encode())
        except:
            self.connected = False

    def loop(self):
        try:
            data = self.sock.recv(10 * 1024).decode()
    
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
        if 'data' in event:
            del event['data']
        
        if '_MESSAGE_HANDLE' in event and event['_MESSAGE_HANDLE'] in self.services:
            service = self.services[event['_MESSAGE_HANDLE']]
            del event['_MESSAGE_HANDLE']
            service(event)
            self.send(sender, event)
            self.receiveChannelEvent(sender, recipient, event)
        
        else:
            
            if '_MESSAGE_ID' in event:
                myCall = self.calls[event['_MESSAGE_ID']]
                if myCall['expiration'] > time.time():
                    response = self.calls[event['_MESSAGE_ID']]
                    response['response'] = event
                    del response['expiration']
                    del response['_MESSAGE_ID']
                    del response['response']['_MESSAGE_ID']
                else:
                    del self.calls[event['_MESSAGE_ID']]
                    
            else:
                self.receiveChannelEvent(sender, recipient, event)
#         else:
#             print('not good -------------- ', filteredEvent)

    def receiveChannelEvent(self, sender, recipient, event):
        if recipient in self.receivers and self.receivers[recipient] != None:
            for x in self.receivers[recipient]:
                x(sender, recipient, event)

    def send(self, channelName, data):
        self.internalSend('sendraw {0} {1}'.format(channelName, json.dumps(data)))

    def call(self, channelName, callName, data, timeout = 1):
        data['_MESSAGE_HANDLE'] = callName 
        data['_MESSAGE_ID'] = uuid.uuid4().__str__()
        self.calls[data['_MESSAGE_ID']] = {'_MESSAGE_HANDLE': callName, '_MESSAGE_ID': data['_MESSAGE_ID'], 'expiration': time.time() + timeout}
        self.send(channelName, data)
        return self.calls[data['_MESSAGE_ID']]
        

    def callAndWait(self, channelName, callName, data, timeout = 1):
        call = self.call(channelName, callName, data, timeout)
        expiration = time.time() + timeout
        while time.time() < expiration:
            time.sleep(0.1)
            if 'response' in call:
                break;
            #         self.calls.append
        return call

    def register(self, channelName, callName, callback):
        self.services[callName] = callback
        self.internalSend('subscribe {0}'.format(channelName))
        self.log('registered responder on {0} for {1}'.format(channelName, callName))

    def subscribe(self, channelName, f):
        if channelName in self.receivers:
            self.receivers[channelName].append(f)
        else:
            self.receivers[channelName] = [f]
        self.internalSend('subscribe {0}'.format(channelName))
        self.log('subscribed to {0}'.format(channelName))
    
    def unsubscribe(self, channelName):
        del self.receivers[channelName]
        self.internalSend('unsubscribe {0}'.format(channelName))
        self.log('unsubscribed from {0}'.format(channelName))

    def variable(self, channelName, key):
        return OOCSIVariable(self, channelName, key)

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
                self.parent.log('re-connecting to OOCSI')
                time.sleep(5)

        self.parent.log('closing connection to OOCSI')

    def __stop(self):
        self.parent.stop()
        return threading.Thread.__stop(self) 


class OOCSICall:
    
    def __init__(self, parent=None):
        self.uuid = uuid.uuid4()
        self.expiration = time.time()
        

class OOCSIVariable(object):
    def __init__(self, oocsi, channelName, key):
        self.key = key
        self.channel = channelName
        oocsi.subscribe(channelName, self.internalReceiveValue)
        self.oocsi = oocsi
        self.value = None 
    def get(self):
        return self.value
    def set(self, value):
        self.value = value
        self.oocsi.send(self.channel, {self.key: value})
    def internalReceiveValue(self, sender, recipient, data):
        if self.key in data:
            self.value = data[self.key]


        
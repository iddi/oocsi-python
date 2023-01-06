import unittest
import time
from oocsi import OOCSI

class TestOOCSICommunication(unittest.TestCase):

    def test_call_response(self):
        
        def respondToEvent(response):
            # set data field in the response
            response['newColor'] = int(response['oldColor']) + 1
    
        # start responder OOCSI client
        # responder = OOCSI('callResponseResponder', 'localhost')
        responder = OOCSI()
        
        # register responder
        responder.register('colorChannel', 'colorGenerator', respondToEvent)
                
        ### test colorGenerator with two calls
        
        # start caller OOCSI client
        #caller = OOCSI('callResponseSender', 'localhost')
        caller = OOCSI()
        self.assertTrue(caller.connected)
        
        # asynchronous call
        call1 = caller.call('colorChannel', 'colorGenerator', {'oldColor': 9}, 1)
        # wait for 500 ms
        time.sleep(0.5)
        
        self.assertEqual(10, call1['response']['newColor'])
                
        # blocking call
        call2 = caller.callAndWait('colorChannel', 'colorGenerator', {'oldColor': 19}, 1)
        
        self.assertEqual(20, call2['response']['newColor'])
        
        caller.stop()
        responder.stop()


    def testChannelCommunication(self):
        
        eventSink = []
        
        def receiveEvent(sender, recipient, event):
            eventSink.append(event)
        
        o1 = OOCSI()
        o1.subscribe('testchannel', receiveEvent)

        o2 = OOCSI()
        
        message = {}
        message['color'] = int(400)
        message['position'] = int(255)
        o2.send('testchannel', message)

        time.sleep(0.5)

        self.assertEquals(1, len(eventSink))

        o1.stop()
        o2.stop()


    def testChannelCommunicationBurst(self):
        
        eventSink = []
        
        def receiveEvent(sender, recipient, event):
            eventSink.append(event)
        
        o11 = OOCSI()
        o11.subscribe('testchannel_b', receiveEvent)
        o12 = OOCSI()
        o12.subscribe('testchannel_b', receiveEvent)
        o13 = OOCSI()
        o13.subscribe('testchannel_b', receiveEvent)

        o2 = OOCSI()
        
        message = {}
        message['burst'] = int(400)
        o2.send('testchannel_b', message)

        time.sleep(0.5)

        self.assertEquals(3, len(eventSink))

        o11.stop()
        o12.stop()
        o13.stop()
        o2.stop()


    def testChannelCommunicationPingPong(self):
                
        eventSink = []
        o1 = OOCSI()
        o2 = OOCSI()
        
        def receiveEventPing(sender, recipient, event):
            count = int(event['ping'])-1
            if count > 0:
                message = {}
                message['ping'] = count
                o2.send('testchannel_pingpong', message)
                eventSink.append(1)
        def receiveEventPong(sender, recipient, event):
            count = int(event['ping'])-1
            if count > 0:
                message = {}
                message['ping'] = count
                o1.send('testchannel_pingpong', message)
                eventSink.append(1)
        
        o1.subscribe('testchannel_pingpong', receiveEventPong)
        o2.subscribe('testchannel_pingpong', receiveEventPing)
        
        message = {}
        message['ping'] = 101
        o1.send('testchannel_pingpong', message)

        time.sleep(2)

        self.assertEquals(100, len(eventSink))

        o1.stop()
        o2.stop()


    def testDirectCommunication(self):
        
        eventSink = []
        
        def receiveEvent(sender, recipient, event):
            eventSink.append(event)
        
        o1 = OOCSI(handle='testclient1', callback=receiveEvent)

        o2 = OOCSI()
        
        message = {}
        message['color'] = int(400)
        message['position'] = int(255)
        o2.send('testclient1', message)

        time.sleep(0.5)

        self.assertEquals(1, len(eventSink))

        o1.stop()
        o2.stop()


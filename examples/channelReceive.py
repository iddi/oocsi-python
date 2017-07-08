from oocsi import OOCSI

def receiveEvent(sender, recipient, event):
    print('from ', sender, ' -> ', event)

o = OOCSI('testreceiver', 'localhost', 4444)
o.subscribe('testchannel', receiveEvent)

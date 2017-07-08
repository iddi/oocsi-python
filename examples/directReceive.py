from oocsi import OOCSI

def receiveEvent(sender, recipient, event):
    print('from ', sender, ' -> ', event)

o = OOCSI('testreceiver', 'localhost', port=4444, callback=receiveEvent)

from oocsi import OOCSI
import time
from random import random

o = OOCSI('testsender', 'localhost', 4444)

while 1:   
    message = {}
    message['color'] = int(random() * 400)
    message['position'] = int(random() * 255)

    o.send('testreceiver', message)

    # wait and continue
    time.sleep(1)

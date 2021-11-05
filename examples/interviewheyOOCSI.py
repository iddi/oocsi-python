import sys
sys.path.append('oocsi')
from oocsi import OOCSI, heyoocsi
import time
import importlib.util
from random import random

# dictionary sender
o = OOCSI('testsender', '192.168.137.122')

# dictionary
prototype = heyoocsi(o,"myfirstprototype")

# dictionary creator
prototype.add_binary_sensor("sensor_name", "sensor_channel", "sensor_type", "sensor_default")
prototype.add_switch("switchname", "sensor_channel", "switch", "false","lightbulb")
prototype.send()

while 1:
    message = {}
    message['state'] = True
    o.send('sensor_channel', message)
    time.sleep(2)
    message2 = {}
    message2['state'] = False
    o.send('sensor_channel', message2)
    time.sleep(2)
    # wait and continue
    
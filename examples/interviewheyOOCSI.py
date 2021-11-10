from oocsi import OOCSI, heyoocsi
import time
from random import random

# oocsiConnection
o = OOCSI('testsender', 'localhost')

# oocsiDevice
# easy approach:
prototype = o.heyOOCSI()

# hard approach:
# prototype = heyoocsi(o,"myfirstprototype")
# (for multiple digital oocsiDevices)

# oocsiEntities for the prototype:
prototype.add_binary_sensor("sensor_name", "sensor_channel", "sensor_type", "sensor_default")
prototype.add_binary_sensor("sensor_name2", "sensor_channel2", "sensor_type", "sensor_default")
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
    
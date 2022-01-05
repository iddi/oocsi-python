# Copyright (c) 2017-2022 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

from oocsi import OOCSI
import time
from random import random

# oocsiConnection
o = OOCSI('testHeyOOCSI', 'localhost')

# create OOCSIDevice -----------------------------------------------------------------------------

# default name for device = the client name "testHeyOOCSI"
device = o.heyOOCSI()

# alternative: named device (for multiple digital oocsiDevices):
# device = o.heyOOCSI("my_first_device")

# add example for location
device.addLocation("kitchen")

# create entities for the device:
# a sensor with name, channel, type, unit and default value 100
device.addSensor("sensor_name", "sensor_channel", "sensor_type", "sensor_unit", 100)
# a binary sensor with name, channel, type, default value, and icon name 
device.addBinarySensor("binary_sensor_name", "sensor_channel2", "sensor_type", False, "binary_icon")
# a switch with name, channel, default value and icon name
device.addSwitch("switch_name", "switch_channel", False, "switch_icon")
# a number with name, channel, min/max, unit, default value and icon name
device.addNumber("number_name", "number_channel", [1, 10], "score", 6, "score_icon")
# a light with name, channel, LED type, spectrum, default value, brightness default, min/max, and icon name
device.addLight("light_name", "light_channel", "RGBW", "WHITE", False, 0, [0, 255], "lamp")

# don't forget to send the description off to the OOCSI server
device.sayHi()

# -----------------------------------------------------------------------------------------------

# run normal device-OOCSI communication with random messages
# that activate and deactivate the entities
while 1:
    # sensor data: random
    messageS = {}
    messageS['value'] = random()
    o.send('sensor_channel', messageS)
    time.sleep(1)
    
    # binary sensor data: on/off
    messageBS = {}
    messageBS['state'] = True
    o.send('sensor_channel2', messageBS)
    time.sleep(0.5)
    messageBS['state'] = False
    o.send('sensor_channel2', messageBS)
    time.sleep(1)
    
    # switch data: off/on
    messageSW = {}
    messageSW['state'] = False
    o.send('switch_channel', messageSW)
    time.sleep(0.5)
    messageSW['state'] = True
    o.send('switch_channel', messageSW)
    time.sleep(1)
    
    # number data: random
    messageN = {}
    messageN['value'] = (random() * 100) % 10
    o.send('number_channel', messageN)
    time.sleep(1)
    
    # light data: random
    messageL = {}
    messageL['state'] = True
    messageL['color_temp'] = (random() * 100) % 10
    messageL['brightness'] = 180
    messageL['colorrgbw'] = 10
    o.send('light_channel', messageL)
    time.sleep(0.7)
    messageL['state'] = True
    messageL['color_temp'] = (random() * 100) % 10
    messageL['brightness'] = 20
    messageL['colorrgbw'] = 100
    o.send('light_channel', messageL)
    time.sleep(0.7)
    messageL['state'] = False
    messageL['color_temp'] = (random() * 100) % 10
    messageL['brightness'] = 120
    messageL['colorrgbw'] = 200
    o.send('light_channel', messageL)
    time.sleep(1)
    # wait and continue
    
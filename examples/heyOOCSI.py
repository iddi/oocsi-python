from oocsi import OOCSI
import time

# oocsiConnection
o = OOCSI('testHeyOOCSI', 'localhost')

# create OOCSIDevice -----------------------------------------------------------------------------

# default name for device:
device = o.heyOOCSI()

# named device (for multiple digital oocsiDevices):
# device = o.heyOOCSI("my_first_device")

# create entities for the device:

# TODO document calls 
device.add_binary_sensor_brick("sensor_name", "sensor_channel", "sensor_type", "sensor_default")
# TODO document calls 
device.add_binary_sensor_brick("sensor_name2", "sensor_channel2", "sensor_type", "sensor_default")
# TODO document calls 
device.add_switch_brick("switchname", "sensor_channel", "switch", "false", "lightbulb")

# TODO add all remaining calls 

# TODO add example for property

# TODO add example for location
 

# don't forget to send the description off to the OOCSI server
device.sayHi()

# -----------------------------------------------------------------------------------------------

# run normal device-OOCSI communication 
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
    
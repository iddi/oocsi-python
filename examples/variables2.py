# Copyright (c) 2017-2022 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

from oocsi import OOCSI
import time


# start responder OOCSI client
responder = OOCSI('variable1', 'localhost')
# create variable 'color' for first client
v1 = responder.variable('colorChannel', 'color')
v1p = responder.variable('colorChannel', 'position')

# start caller OOCSI client
caller = OOCSI('variable2', 'localhost')
# create variable 'color' for second client
v2 = caller.variable('colorChannel', 'color')
v2p = caller.variable('colorChannel', 'position')

# assign a string
v1.set(40)
v1p.set(210)
print('value of first color: ', v1.get())
print('value of first position: ', v1p.get())

time.sleep(0.1)

print('value of second color: ', v2.get())
print('value of second position: ', v2p.get())


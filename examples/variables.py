# Copyright (c) 2017-2022 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

from oocsi import OOCSI
import time


# start responder OOCSI client
responder = OOCSI('variable1', 'localhost')
# create variable 'color' for first client
v1 = responder.variable('colorChannel', 'color')

# start caller OOCSI client
caller = OOCSI('variable2', 'localhost')
# create variable 'color' for second client
v2 = caller.variable('colorChannel', 'color')

# assign an int
v1.set(100)
print('value of first variable: ', v1.get())

time.sleep(0.1)

print('value of second variable: ', v2.get())

# assign a float
v2.set(200.1)
print('value of second variable: ', v2.get())

time.sleep(0.1)

print('value of first variable: ', v1.get())

# assign a string
v1.set('hello world')
print('value of first variable: ', v1.get())

time.sleep(0.1)

print('value of second variable: ', v2.get())

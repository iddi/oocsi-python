# Copyright (c) 2017-2022 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

from oocsi import OOCSI
import time
from random import random

o = OOCSI('testsender', 'localhost')

while 1:   
    message = {}
    message['color'] = int(random() * 400)
    message['position'] = int(random() * 255)

    o.send('testchannel', message)

    # wait and continue
    time.sleep(1)

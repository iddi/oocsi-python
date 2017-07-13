# Copyright (c) 2017 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

from oocsi import OOCSI

def receiveEvent(sender, recipient, event):
    print('from ', sender, ' -> ', event)

o = OOCSI('testreceiver', 'localhost')
o.subscribe('testchannel', receiveEvent)

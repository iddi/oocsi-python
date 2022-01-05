# Copyright (c) 2017-2022 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

from oocsi import OOCSI

def receiveEvent(sender, recipient, event):
    print('from ', sender, ' -> ', event)

o = OOCSI('testreceiver', 'localhost', callback=receiveEvent)

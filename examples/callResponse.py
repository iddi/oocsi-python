# Copyright (c) 2017 Mathias Funk
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

import time
from oocsi import OOCSI

def respondToEvent(response):
    # set data field in the response
    response['newColor'] = int(response['oldColor']) + 1
    
    # play with this delay to let the caller time out
    # time.sleep(4)

# start responder OOCSI client
# responder = OOCSI('callResponseResponder', 'localhost')
responder = OOCSI()
print(responder.handle)

# register responder
responder.register('colorChannel', 'colorGenerator', respondToEvent)


### test colorGenerator with two calls

# start caller OOCSI client
#caller = OOCSI('callResponseSender', 'localhost')
caller = OOCSI()
print(caller.handle)

# asynchronous call
call1 = caller.call('colorChannel', 'colorGenerator', {'oldColor': 9}, 1)
# wait for 1 sec
time.sleep(1)

# check response in call object
if 'response' in call1:
    print(call1['response'])
else:
    print('response not found')

# blocking call
call2 = caller.callAndWait('colorChannel', 'colorGenerator', {'oldColor': 19}, 1)
# check response in call object directly
if 'response' in call2:
    print(call2['response'])
else:
    print('response not found')

caller.stop()
responder.stop()

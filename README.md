# oocsi-python
Python client library for [OOCSI](https://github.com/iddi/oocsi). OOCSI is a multi-platform communication framework that allows for easy messaging between clients. OOCSI is light-weight, message-oriented, allows for point-to-point messaging and broadcasting to channels (or topics). The Python client library allows to connect from Python to an OOCSI server and to communicate with other OOCSI clients, on Python or on different platforms such as plain Java, Processing, Android, Websocket or Arduino ESP.

## Installation
Installing the OOCSI library is very straight-forward for Python:

```bash
pip install oocsi
```

## Usage
To use OOCSI on Python, we first need to connect to OOCSI. Then we can send and receive messages. This example follows the channel send and receive example that can be found in the [examples](examples/) folder.

### Connect
The first step is to connect to a OOCSI server, either running on the local machine (see here how to do that) or on a publicly accessible server. To connect, you will need the server address and also create a unique handle for this client. This handle will be used to identify the client when other clients send messages to it. A handle is composed of ASCII characters, but cannot contain spaces.

```python
from oocsi import OOCSI

# connect OOCSI running on the local machine ('localhost')
oocsi = OOCSI('Alice', 'localhost')

# connect OOCSI running on a webserver
oocsi = OOCSI('Alice', 'oocsi.example.com')

# connect OOCSI running on a webserver with a custom port (4545)
oocsi = OOCSI('Alice', 'oocsi.example.com', 4545)
```  
In case the connection fails, the error will be printed on the Python console. The most common reason that a client fails connecting is because the client's chosen handle is already active on the server. Choosing a slightly different handle will then solve the problem.


### Sending messages (asynchronous)

Now that the client Alice is connected to OOCSI, the client can send messages to others in the network. The recipients of messages can be either handles of other clients (direct communication, point-to-point) or the name of a channel (broadcasting).

```python
# send a message to client Bob with data (as a Dict)
oocsi.send('Bob', {'color': 120})

# send a message to channel coloChannel with data (as a Dict)
oocsi.send('colorChannel', {'color': 120})
```  

### Receiving messages
Messages from OOCSI that are sent directly to thsi client (using the handle Alice in the example), can be received using a callback that is provided when connecting. In the example below, all direct messages to Alice are received through the callback handleDirectMessage. This callback method receives the sender of the message, the recipient (channel name) and the event data as arguments. 

```python
from oocsi import OOCSI

def handleDirectMessage(sender, recipient, event):
  print(event['color'])

# connect and provide callback for messages sent directly to Alice
oocsi = OOCSI('Alice', 'localhost', callback=handleDirectMessage)

```  

Messages from OOCSI channels can be received by subscribing to channels callbacks. In the example below, the client Alice subscribes to a channel colorchannel and receives events to this channel via the callback handleColorEvent. This callback method receives the sender of the message, the recipient (channel name) and the event data as arguments. The recipient is added to allow for distinguishing messages when subscribing to multiple channels with the same callback.

```python
from oocsi import OOCSI

def handleColorEvent(sender, recipient, event):
  print(event['color'])

# connect 
oocsi = OOCSI('Alice', 'localhost')

# subscribe to channel testchannel with a callback handleColorEvent
oocsi.subscribe('testchannel', handleColorEvent)
```  

### Sending messages (synchronous)
Clients can send messages to others in the network also in a synchronous way. That means, that the client sends a message to another client and waits for a corresponding reply message. This is useful for queries for data or remote processing of data by another client.
This mechanism is shown in the [call-response](examples/callResponse.py) example.


### OOCSI Variables
OOCSI can work with variables that are automatically synchronized over channels in the OOCSI network. A variable is created by a client for a channel on a key of a message. Whenever a message with that key is received over the channel the variable is locally updated, and whenever the local variable is set by the client, it will send out the new value on the given channel. 

```python
from oocsi import OOCSI

# connect 
oocsi = OOCSI('Alice', 'localhost')

# subscribe to channel testchannel with a callback handleColorEvent
color = oocsi.variable('colorchannel', 'color')

# set the variable 
color.set(255)

# get the variable's value
color.get()

```  


This mechanism is shown more detail in the [variables](examples/variables.py) example. In the OOCSI Python client, variables do not have different types such as int, float or string. Therefore, checking the content of the variable might be advisable before using it.  
 


## Limitations
At the moment, a subset of functionality that is available in the OOCSI Java implementation is implemented for Python. Beyond the basic communication framework, higher level functions like synchronization, negotiation etc are yet to be implemented.


## API Reference
Tbd.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

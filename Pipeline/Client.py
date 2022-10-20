#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import json

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  request and wait for a response
print(f"Sending request…")
socket.send_string("A message from CS361")

#  Get the reply.
message = json.loads(socket.recv_string())
print(f"Received reply [ {message} ]")

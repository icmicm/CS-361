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
socket.send_pyobj({"sex": "Men", "category": "Lightweight", "origin": "Japan"})

#  Get the reply.
message = socket.recv_pyobj()
print(f"Received reply!")
print(message)

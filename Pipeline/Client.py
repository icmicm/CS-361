
import json

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  request and wait for a response
print(f"Sending request…")
#socket.send_pyobj({"country": "Canada"})
socket.send_pyobj({"olympic": "2020"})
socket.send_pyobj({"sex": "Men", "category": "Lightweight", "origin": "Japan"})

#  Get the reply.
message = socket.recv_pyobj()
print(f"Received reply!")
print(message)

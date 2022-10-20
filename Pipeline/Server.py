#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
import json
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_string()
    print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(1)

    #  Send reply to client
    socket.send_string(json.dumps({"data": ["a", "b", "c"]}))

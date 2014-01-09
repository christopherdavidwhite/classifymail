#!/home/christopher/anaconda/bin/python2

import sys
import zmq

if __name__ == "__main__":

    msgstr = sys.stdin.read()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    socket.send(msgstr)
    c = socket.recv()
    print c

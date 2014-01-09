#!/home/christopher/anaconda/bin/python2

from email.parser  import Parser
import pickle
import sys
import zmq
import os

#modified from http://nltk.org/api/nltk.classify.html
def minimal_features(msg):
    payload = msg.get_payload()
    while type(payload) is list:
        payload = payload[0].get_payload()

    words = payload.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Binary classification of email.')
    parser.add_argument('-c', '--classifier', action="store", dest="cfn", 
                        default="/home/christopher/.classifymail_classifier")
    parser.add_argument('-i', '--ipc-path', action="store", dest="ipc_path", 
                        default='tcp://127.0.0.1:5555')
    args = parser.parse_args()

    f= open(args.cfn)
    c = pickle.load(f)
    f.close()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    rc = socket.bind('tcp://127.0.0.1:5555')

    while True:
        msgstr = socket.recv()
        P = Parser() #MIME parser
        msg = P.parsestr(msgstr)
        socket.send(c.classify(minimal_features(msg)))



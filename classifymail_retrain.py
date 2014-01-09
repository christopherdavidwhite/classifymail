#!/home/christopher/anaconda/bin/python2

from email.parser  import Parser
from email.utils   import parsedate
from time          import mktime
from nltk.classify import NaiveBayesClassifier
from os            import listdir
from classifymail_server  import minimal_features
import pickle
import sys

#Takes a file name of a message: opens, parses, closes, returns parsed message
def parsefn(fn):
    f = open(fn, "r")
    msg = P.parse(f) #P is a parser constructed once in main.
    f.close()
    return(msg)

def reload_msgs(posdir, alldir):
    posmsgs = [parsefn(posdir + "/" + msgfn) for msgfn in listdir(posdir)]
    posMIDs = [msg['Message-ID'] for msg in posmsgs]
    minpostime = min([mktime(d) 
                      for d in 
                      [parsedate(msg['Date']) for msg in posmsgs] 
                      if not(None == d)])

    negmsgs = []
    for msgfn in listdir(alldir):
        path = alldir + "/" + msgfn
        msg = parsefn(path)
        if msg['Date'] != None:
            if (mktime(parsedate(msg['Date'])) > minpostime and not(msg['Message-ID'] in posMIDs)):
                negmsgs.append(msg)
    return(posmsgs, negmsgs)

def retrain(posmsgs, negmsgs):
    postrain = [(minimal_features(msg), 'positive')  for msg in posmsgs]
    negtrain = [(minimal_features(msg), 'negative') for msg in negmsgs]

    return(NaiveBayesClassifier.train(postrain + negtrain))

if __name__ == "__main__":
    import argparse
    P = Parser() #MIME parser

    parser = argparse.ArgumentParser(description='Binary classification of email.')
    parser.add_argument('-c', '--classifier', action="store", dest="cfn", 
                        default="/home/christopher/.classifymail_classifier")
    parser.add_argument('-p', '--positive', action="store", dest="posdir",
                        default="/home/christopher/mail/important/cur")
    parser.add_argument('-a', '--all',      action="store", dest="alldir",
                        default="/home/christopher/mail/primary/cur") 
    args = parser.parse_args()

    (posmsgs, negmsgs) = reload_msgs(args.posdir, args.alldir)
    c = retrain(posmsgs, negmsgs)

    f = open(args.cfn, "wb")
    pickle.dump(c, f)
    f.close()

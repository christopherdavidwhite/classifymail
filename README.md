classifymail
============

Machine-learning classification of email

 * classifymail_server keeps the (large) classifier in memory. It takes MIME messages via 0MQ req-reply and replies with 'positive' or 'negative'
 * classifymail_retrain trains a new classifier on one directory full of "positive" messages and one containing a combination of "negative" and the same messages as in the "positive" (so if you're nervous about changing your email setup, as I was, you can just copy the positive messages out). It does not train (either way) on messages earlier than the earliest given "positive" message. The directories are hard-coded at the moment.
 * classifymail reads a message from stdin, passes it to classifymail_server, and prints the server's reply

I use with getmail and procmail (and mutt). 

In my .getmailrc:

    [filter-bayes]
    type = Filter_classifier
    path = /home/christopher/bin/classifymail #this is a link to the client

In my .procmailrc:

    :0
    *X-getmail-filter-classifier: positive
    $MAILDIR/important/

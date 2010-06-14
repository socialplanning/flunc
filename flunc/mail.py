"""
Extensions for mail functions -- both testing sending mail
to a server, and testing mail that is sent by a server.

These extensions are pretty specific to my immediate need,
which is writing tests for Listen.

The extensions assume that the server is using 
 http://github.com/ejucovy/Products.FileWritingMailHost/
which writes out mails to files instead of sending them,
and injects headers into the request to tell the client
where to find the mails.  The expected setup for these tests
has the client and server on the same physical machine,
so that the client can simply read the mail files written
by the server.
"""

from flunc._mail import send

def send_mail(file):
    fp = open(file)
    mailStr = fp.read()
    fp.close()

    mails = send(receiverURL, mailStr)
    if mails is None:
        return
    

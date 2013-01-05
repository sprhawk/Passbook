#! /Usr/bin/python
# -*- coding: utf-8 -*-

import testpass
import os
import sys

#usage: python test.py your_key_passphrase
if __name__ == "__main__":
    cwd = os.getcwd()
    keyfile =  "your.key.pem"
    certfile=  "your.cert.pem"
    wwdrfile=  "AppleWWDRCA.pem"
    p = testpass.getTestPass()
    wwdr = open(wwdrfile, 'rb').read()
    cert = open(certfile, 'rb').read()
    key = open(keyfile, 'rb').read()
    zipdata = p.getSignedPass(wwdr, cert, key, sys.argv[1])
    open('test.pkpass', 'wb').write(zipdata)



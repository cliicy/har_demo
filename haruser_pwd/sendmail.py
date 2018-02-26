#!/usr/local/bin/python

import xmlrpclib
import sys


try:
    s = xmlrpclib.ServerProxy('http://UDPv5-60455:2332')
    s.sendmail(sys.stdin.read())
except:
    pass


#!/usr/bin/env python
# coding=utf-8

import sys
import os
import json
from urllib2 import Request, urlopen, URLError, HTTPError
from argparse import ArgumentParser
from zeroconf import ServiceBrowser, Zeroconf

usage = 'Usage: python {} remo [-g|-p] [-f nickname]'.format(__file__)
argparser = ArgumentParser(usage=usage)
argparser.add_argument('remo', type=str, help="remo hostname")
argparser.add_argument('-g', '--get',    action='store_true', dest='get',    default=False, help='get message')
argparser.add_argument('-p', '--post',   action='store_true', dest='post',   default=False, help='post message')
argparser.add_argument('-f', '--file',   type=str, dest='file', default="-", help='signal file')
args = argparser.parse_args()

def get_json(name):
    if name == '-':
        return sys.stdin.read()
    else:
        with open(name) as f:
            return f.read()


url = 'http://' + args.remo + '/messages'
headers = { }
headers["X-Requested-With"] =  "curl"
if args.post:
    headers["Content-Type"] = "application/json" 
data = None
if args.post:
    data = get_json(args.file)

req = Request(url, data=data, headers=headers)
body = urlopen(req).read()
print(body)

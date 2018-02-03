#!/usr/bin/env python
# coding=utf-8

import sys
import os
import json
from urllib2 import Request, urlopen, URLError, HTTPError
from argparse import ArgumentParser

BASE_URL = "https://api.nature.global"
BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE      = os.path.join(BASE_PATH, 'token.txt')
APPLIANCES_FILE = os.path.join(BASE_PATH, 'appliances.json')

usage = 'Usage: python {} command [--dev_no dev_no] [--nickname nickname] [--name name]'.format(__file__)
argparser = ArgumentParser(usage=usage)
argparser.add_argument('command', type=str, help='[get_temp|get_appliances|send_signal]')
argparser.add_argument('-d', '--dev_no', type=int, dest='dev_no', help='device number for reading temperature')
argparser.add_argument('-a', '--nickname', type=str, dest='nickname', help='appliance name')
argparser.add_argument('-n', '--name', type=str, dest='name', help='signal name')
args = argparser.parse_args()

def get_token():
    f = open(TOKEN_FILE, 'r')
    token = f.read().strip()
    f.close()
    return token

def get_signal_id(nickname, name):
    f = open(APPLIANCES_FILE, 'r')
    json_dict = json.load(f)
    for appliance in json_dict:
        if appliance['nickname'] != nickname:
            continue
        for signal in appliance['signals']:
            if signal['name'] == name:
                return signal['id']
    f.close()
    return None

url = BASE_URL
data = None
if args.command =='get_temp':
    url += "/1/devices"
elif args.command == 'get_appliances':
    url += "/1/appliances"
elif args.command == 'send_signal':
    nickname = args.nickname.decode('utf-8')
    name = args.name.decode('utf-8')
    signal_id = get_signal_id(nickname, name)
    url += "/1/signals/" + signal_id + "/send"
    data = "\r\n"
else:
    print "Command error: ", args.command
    sys.exit(1)
# print url

token = get_token()
headers = { "Authorization" : "Bearer " + token }
req = Request(url, data=data, headers=headers)
try:
    res = urlopen(req)
except HTTPError, e:
    print 'Error code: ', e.getcode()
    sys.exit(1)
except URLError as e:
    print 'Reason: ', e.reason
    sys.exit(1)

body = res.read()
if args.command == 'get_temp':
    body = json.loads(body)[args.dev_no]['newest_events']
    body = json.dumps(body)

print body

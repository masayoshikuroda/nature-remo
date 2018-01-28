#!/usr/bin/env python
# coding=utf-8

import sys
import os
import json
import urllib2

BASE_URL = "https://api.nature.global"
BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE      = os.path.join(BASE_PATH, 'token.txt')
APPLIANCES_FILE = os.path.join(BASE_PATH, 'appliances.json')

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

if len(sys.argv) <= 2:
    print 'Usage: python remo.py appliance_name, signal_name'
    sys.exit(1)

nickname = sys.argv[1].decode('utf-8')
name = sys.argv[2].decode('utf-8')

token = get_token()
signal_id = get_signal_id(nickname, name)

url = BASE_URL + "/1/signals/" + signal_id + "/send"
headers = { "Authorization" : "Bearer " + token }
req = urllib2.Request(url, data="\r\n", headers=headers)
try:
    res = urllib2.urlopen(req)
except HTTPError, e:
    print e.getcode()
print res.getcode()

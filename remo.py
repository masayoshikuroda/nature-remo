#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError, HTTPError
from argparse import ArgumentParser

BASE_URL        = "https://api.nature.global"
BASE_PATH       = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE      = os.path.join(BASE_PATH, 'token.txt')
APPLIANCES_FILE = os.path.join(BASE_PATH, 'appliances.json')

usage = 'Usage: python {} command [--dev_no dev_no] [--app_no app_no] [--nickname nickname] [--name name]'.format(__file__)
commands = '|'.join(['list_devices', 'list_appliances', 'get_appliances', 'get_events', 'post_signal', 'post_aircon', 'get_smartmeter'])
argparser = ArgumentParser(usage=usage)
argparser.add_argument('command', type=str, help=commands)
argparser.add_argument('-d', '--dev_no',   type=int, dest='dev_no', default=0, help='device number for reading temperature')
argparser.add_argument('-a', '--app_no',   type=int, dest='app_no', default=0, help='appliance number for reading smartmeter')
argparser.add_argument('-n', '--nickname', type=str, dest='nickname', help='appliance name')
argparser.add_argument('-s', '--name',     type=str, dest='name',     help='signal name')
argparser.add_argument('-t', '--temp',     type=str, dest='temp',     help='aircon temperature [-2|-1|0|1|2]]')
argparser.add_argument('-m'  '--mode',     type=str, dest='mode',     help='aircom operating mode [cool|warm|dry|blow|auto]')
argparser.add_argument('-v', '--volume',   type=str, dest='volume',   help='aircon air volume [1|auto]')
argparser.add_argument('-i', '--dir',      type=str, dest='dir',      help='aircon air direction [auto|still]')
argparser.add_argument('-b', '--button',   type=str, dest='button',   help='aircon button [power-off]')
args = argparser.parse_args()

def get_token():
    f = open(TOKEN_FILE, 'r')
    token = f.read().strip()
    f.close()
    return token

def get_appliance(nickname):
    appliances = []
    with open(APPLIANCES_FILE, 'r') as f:
        appliances = json.load(f)

    matched = filter(lambda a:a['nickname'] == nickname, appliances)
    if len(matched) == 0:
        raise ValueError(nickname)
    return matched[0]

def get_appliance_id(nicnname):
    appliance = get_appliance(nickname)
    return appliance['id']

def get_signal(nickname, name):
    appliance = get_appliance(nickname)
    signals = appliance['signals']

    matched = filter(lambda s:s['name'] == name, signals)
    if len(matched) == 0:
        raise ValueError(name)
    return matched[0]

def get_signal_id(nickname, name):
    signal = get_signal(nickname, name)
    return signal['id']

url = BASE_URL
data = None
if args.command.startswith('list_dev'):
    url += "/1/devices"
elif args.command.startswith('list_app'):
    url += "/1/appliances"
elif args.command.startswith('get_eve'):
    url += "/1/devices"
elif args.command.startswith('get_app'):
    url += "/1/appliances"
elif args.command.startswith('get_sma'):
    url += "/1/appliances"
elif args.command.startswith('post_sig'):
    nickname = args.nickname.decode('utf-8')
    name = args.name.decode('utf-8')
    signal_id = get_signal_id(nickname, name)
    url += "/1/signals/" + signal_id + "/send"
    data = "\r\n"
elif args.command.startswith('post_aircon'):
    nickname = args.nickname.decode('utf-8')
    appliance_id = get_appliance_id(nickname)
    url += "/1/appliances/" + appliance_id + "/aircon_settings"
    data = {}
    if args.temp is not None:
        data["temperature"] = args.temp
    if args.mode is not None:
        data["operation_mode"] = args.mode
    if args.volume is not None:
        data["air_volume"] = args.volume
    if args.dir is not None:
        data["air_direction"] = args.dir
    if args.button is not None:
        data["button"] = args.button
    print(data)
    data = urlencode(data)
else:
    print("Command error: ", args.command)
    sys.exit(1)
#print(url)

token = get_token()
headers = { "Authorization" : "Bearer " + token }
req = Request(url, data=data, headers=headers)
try:
    res = urlopen(req)
except HTTPError as e:
    print('Error code: ', e.getcode())
    sys.exit(1)
except URLError as e:
    print('Reason: ', e.reason)
    sys.exit(1)

body = res.read().decode()
#print(body)

if args.command.startswith('list_dev'):
    devices = json.loads(body)
    body = ""
    for i, device in enumerate(devices):
        body += str(i) + "," 
        body += json.dumps(device['name'], ensure_ascii=False)
        body +=  "\r\n"
elif args.command.startswith('list_app'):
    appliances = json.loads(body)
    body = ""
    for i, appliance in enumerate(appliances):
        body += str(i) + ","
        body += json.dumps(appliance['nickname'], ensure_ascii=False)
        body += "\r\n"
elif args.command.startswith('get_eve'):
    body = json.loads(body)[args.dev_no]['newest_events']
    body = json.dumps(body, ensure_ascii=False)
elif args.command.startswith('get_sma'):
    body = json.loads(body)[args.app_no]['smart_meter']['echonetlite_properties']
    body = json.dumps(body, ensure_ascii=False)    
print(body)

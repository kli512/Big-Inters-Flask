import json
import sys
from collections import defaultdict

import requests

class ServerException(Exception):
    pass

class ClientException(Exception):
    pass

# API Key
_API_KEY = None

# Queue Types
_queues_raw = None
try:
    qr = requests.get('http://static.developer.riotgames.com/docs/lol/queues.json')
    if qr.status_code != 200:
        raise ConnectionError
    _queues_raw = qr.json()
except:
    raise IOError('No queues.json file')
    print('Could not reach Riot for queues file. Falling back on local...', file=sys.stderr)
    with open('RiotAPI/queues.json') as qf:
        _queues_raw = json.load(qf)

ALL_QUEUE_TYPES = {}
for info in _queues_raw:
    try:
        if 'deprecated' in info['notes'].lower():
            continue
    except AttributeError:
        pass
    try:
        desc = info['description'].replace('games', '').strip()
    except AttributeError:
        desc = 'Custom'
    ALL_QUEUE_TYPES[desc] = info['queueId']

_popular_queue_types = {'Custom', '5v5 ARAM', '5v5 Draft Pick', '5v5 Ranked Solo', '5v5 Blind Pick', '5v5 Ranked Flex'}
QUEUE_TYPES = {k: v for k, v in ALL_QUEUE_TYPES.items() if k in _popular_queue_types}

if len(_popular_queue_types) != len(QUEUE_TYPES):
    print('Gamemode listed in _popular_queue_types not found in ALL_QUEUE_TYPES', file=sys.stderr)

# Riot API Requester
class RiotApiRequester:
    def __init__(self, api_key, region):
        self.api_key = api_key
        self.region = region

    def dump_response(self, r):
        msg = f'HTTP Response:\n\t{r}\n\t{r.status_code}\n\t{r.headers}\n\t'
        try:
            msg += r.json()
        except:
            msg += r.content.decode('utf-8')
        print(msg, file=sys.stderr)

    def get(self, url, **kwargs):
        req = f'https://{self.region}.api.riotgames.com{url}?api_key={self.api_key}'
        for arg, vals in kwargs.items():
            for val in vals:
                req += f'&{arg}={val}'
        print(f'Make GET request: "{req}"', file=sys.stderr)
        r = requests.get(req)
        if r.status_code != 200:
            if r.status_code == 403:
                print(f'Forbidden - possibly invalid API key?', file=sys.stderr)
                raise ServerException('Forbidden')
            print(f'Failed GET Request', file=sys.stderr)
            self.dump_response(r)
            raise ClientException('Invalid request')
        return r


import sys
from collections import defaultdict
from typing import Union, List

from BigInters.Analyzer.RiotAPI import RiotAPI
from BigInters.Analyzer.utils import KDA

API_KEY = ''

def run_analysis(summoner: str, n_matches: Union[str, int], queues: Union[List[str], List[int]], region: str):
    print('Starting player analysis', file=sys.stderr)
    n_matches = str(n_matches)
    if n_matches == '':
        n_matches = '10'
    queues = list(map(str, queues))

    RAR = RiotAPI.RiotApiRequester(API_KEY, region)
    summoner_r = RAR.get(
        f'/lol/summoner/v4/summoners/by-name/{summoner}')
    account_eid = summoner_r.json()['accountId']
    matches_r = RAR.get(
        f'/lol/match/v4/matchlists/by-account/{account_eid}', endIndex=[n_matches], queue=queues)
    matches = matches_r.json()['matches']
    player_kdas = defaultdict(lambda: {'encounters': 0, 'kda': KDA()})

    for match in matches:
        match_r = RAR.get(f'/lol/match/v4/matches/{match["gameId"]}')

        players = match_r.json()['participantIdentities']
        players = dict([(player['participantId'], player['player']
                        ['summonerName']) for player in players])

        player_data = match_r.json()['participants']

        for player in player_data:
            summoner_name = players[player['participantId']]
            player_kdas[summoner_name]['encounters'] += 1
            for val in ('kills', 'deaths', 'assists'):
                player_kda = player_kdas[summoner_name]['kda']
                player_kda[val] += player['stats'][val]

    player_kdas = tuple((k, v) for k, v in sorted(
        player_kdas.items(), key=lambda player_data: player_data[1]['encounters'], reverse=True))

    print('Analysis finished', file=sys.stderr)
    return {'requestData': {'summoner': summoner, 'matches': n_matches, 'queues': queues}, 'responseData': player_kdas}

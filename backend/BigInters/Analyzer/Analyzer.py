import sys
from collections import defaultdict
from typing import Union, List

from BigInters.Analyzer.RiotAPI import RiotAPI

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

    player_stats = defaultdict(lambda: {
        'summonerName': None,
        'encounters': 0,
        'wins': 0,
        'kills': 0,
        'deaths': 0,
        'assists': 0,
        'cs': 0,
        'visionScore': 0,
        'damageDealt': 0,
        'gameTime': 0
    })

    for match in matches:
        match_r = RAR.get(f'/lol/match/v4/matches/{match["gameId"]}')
        match_data = match_r.json()

        match_time = match_data['gameDuration']

        players = match_data['participantIdentities']
        players = {player['participantId']: player['player'] for player in players}

        player_data = match_data['participants']

        team_id = list(filter(lambda p: players[p['participantId']]['accountId'] == account_eid, player_data))[0]['teamId']

        for player in player_data:
            if player['teamId'] != team_id:
                continue
            player_info = players[player['participantId']]
            account_id = player_info['accountId']

            player_stats[account_id]['gameTime'] += match_time

            if player_stats[account_id]['summonerName'] == None:
                player_stats[account_id]['summonerName'] = player_info['summonerName']

            player_stats[account_id]['encounters'] += 1

            if player['stats']['win']:
                player_stats[account_id]['wins'] += 1

            game_stats = player['stats']

            for val in ('kills', 'deaths', 'assists', 'visionScore'):
                player_stats[account_id][val] += game_stats[val]

            player_stats[account_id]['cs'] += game_stats['totalMinionsKilled'] + game_stats['neutralMinionsKilled']
            player_stats[account_id]['damageDealt'] += game_stats['totalDamageDealtToChampions']

    print('Analysis finished', file=sys.stderr)
    return {'requestData': {'summoner': summoner, 'matches': n_matches, 'queues': queues}, 'responseData': list(player_stats.values())}

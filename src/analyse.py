#!/usr/bin/env python3
import time
from sys import argv

import requests

try:
    from secrets import lichess_api_token
except ImportError:
    lichess_api_token = ''

if argv[1]:
    cookie = argv[1]

def get_unanalzsed_game(username):
    url = f'https://lichess.org/api/games/user/{username}'
    headers = {
        'Accept': 'application/x-ndjson',
    }
    if lichess_api_token:
        headers['Authorization'] = f'Bearer {lichess_api_token}'
    params = {
        'rated': 'true',
        'perfType': 'blitz',
        'max': 1,
        'analysed': False
    }
    r = requests.get(url, params=params, headers=headers)
    return r.json()['id']


def analyse(game_id):
    headers = {
        'Cookie': cookie
    }
    url = f'https://lichess.org/{game_id}/request-analysis'
    print()
    print(f'Analyzing {game_id}.')

    r = requests.post(url, headers=headers)
    if (r.status_code != 204):
        raise Exception(r)


prev_game_id = 0
while True:
    game_id = get_unanalzsed_game('kewko')
    if game_id != prev_game_id:
        analyse(game_id)
    prev_game_id = game_id
    time.sleep(5)
    print(".", end='')

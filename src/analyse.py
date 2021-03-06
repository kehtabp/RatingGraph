#!/usr/bin/env python3
import time
from sys import argv

import requests

try:
    from secrets import lichess_api_token

    print("Imported token")
except ImportError:
    lichess_api_token = ''

if argv[1]:
    cookie = argv[1]


def get_unanalysed_game(username, count=False):
    url = f'https://lichess.org/api/games/user/{username}'
    headers = {
        'Accept': 'application/x-ndjson',
    }
    if lichess_api_token:
        headers['Authorization'] = f'Bearer {lichess_api_token}'
    params = {
        'rated': 'true',
        'perfType': 'blitz',
        'analysed': False,
        'moves': False,
        'tags': False,
    }
    if not count:
        params['max'] = 1
    r = requests.get(url, params=params, headers=headers)
    if count:
        return len(r.text.split())
    return r.json()['id']


def analyse(game_id):
    headers = {
        'Cookie': cookie
    }
    url = f'https://lichess.org/{game_id}/request-analysis'
    print()
    print(f'Analyzing {game_id}.')

    r = requests.post(url, headers=headers)
    if r.status_code != 204:
        raise Exception(r)


prev_game_id = 0
games_analysed = 0
while True:
    username = 'kewko'
    game_id = get_unanalysed_game(username)
    if game_id != prev_game_id:
        try:
            analyse(game_id)
            games_analysed += 1
        except Exception as e:
            print(f"Done. Analysed {games_analysed} games. {get_unanalysed_game(username,True)} games remaining.")
            break

    prev_game_id = game_id
    time.sleep(5)
    print(".", end='')

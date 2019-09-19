import requests

from get_json import get_json

GAME_MODE = "blitz"


def get_top_players(perf_type, num=100):
    json_file_path = f'data/top_players/lichess_{perf_type}.json'
    url = f'https://lichess.org/player/top/{num}/{perf_type}'
    headers = {
        'Accept': 'application/vnd.lichess.v3+json'
    }
    r = requests.get(url, headers=headers)

    return r.json()['users']


players = get_top_players(GAME_MODE, 100)
for player in players:
    get_json(player['id'], GAME_MODE, analysed="true", ensure_complete=True, maxnum=100)

import time

import requests

try:
    from secrets import lichess_api_token
except ImportError:
    lichess_api_token = ''


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
        'Cookie': 'lila2=53fd4fe392fd4497deaed0f026e493b504ab24ae-sid=vxgIQSbpCw&sessionId=GX9c8JFxFRaEQ63boAWa3R; AMCV_68044180541804760A4C98A5%40AdobeOrg=-1712354808%7CMCIDTS%7C18121%7CMCMID%7C32967858011318067642751201952902946196%7CMCAID%7CNONE%7CMCOPTOUT-1565622181s%7CNONE%7CvVersion%7C4.3.0'
    }
    url = f'https://lichess.org/{game_id}/request-analysis'
    r = requests.post(url, headers=headers)
    print()
    print(f'Analyzing {game_id}. {r}')


prev_game_id = 0
while True:
    game_id = get_unanalzsed_game('kewko')
    if game_id != prev_game_id:
        analyse(game_id)
    prev_game_id = game_id
    time.sleep(5)
    print(".", end='')

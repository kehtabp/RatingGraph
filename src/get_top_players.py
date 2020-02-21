import requests

GAME_MODES = "blitz", "bullet", "classical"


def get_top_players(perf_type, num=100):
    url = f'https://lichess.org/player/top/{num}/{perf_type}'
    headers = {
        'Accept': 'application/vnd.lichess.v3+json'
    }
    r = requests.get(url, headers=headers)

    return r.json()['users']


def get_player_info(username):
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get(f'https://lichess.org/api/user/{username}', headers)
    return r.json()


players = []

for GAME_MODE in GAME_MODES:
    players += get_top_players(GAME_MODE, 1000)
for player in players:
    player = get_player_info(player['id'])
    username = player['username']
    try:
        fide_rating = player['profile']['fideRating']
        title = player['title']
    except:
        continue
    if player['perfs']['blitz']['rd'] <= 65:
        blitz_rating = player['perfs']['blitz']['rating']
    else:
        blitz_rating = ''
    if player['perfs']['bullet']['rd'] <= 65:
        bullet_rating = player['perfs']['bullet']['rating']
    else:
        bullet_rating = ''
    if player['perfs']['classical']['rd'] <= 65:
        classical_rating = player['perfs']['classical']['rating']
    else:
        classical_rating = ''
    print(f"{username},{blitz_rating},{bullet_rating },{classical_rating },{title},{fide_rating}")
# for player in players:
#     get_json(player['id'], GAME_MODE, analysed="true", ensure_complete=True, maxnum=100)

from datetime import datetime
from pathlib import Path

import ndjson
import requests


def get_json(username, game_mode="bullet", update=False):
    json_file_path = f'data\lichess_{username}_{game_mode}.json'
    url = f'https://lichess.org/api/games/user/{username}'
    headers = {
        'Accept': 'application/x-ndjson',
        'Authorisation': 'Bearer fyZlIrDXdDD4Idaf'
    }
    parameters = {
        'rated': 'true',
        'perfType': game_mode
    }
    json_file = Path(json_file_path)
    if not json_file.is_file():
        r = requests.get(url, headers=headers, params=parameters)

        with open(json_file_path, 'wb') as f:
            f.write(r.content)
    with open(json_file, 'r') as file:
        json_games = ndjson.loads(file.read())
        since = json_games[0]['createdAt']
        parameters['since'] = since

        if not update:
            return json_games

        r = requests.get(url, headers=headers, params=parameters)
        new_games = ndjson.loads(r.content)
        if new_games:
            print(f'Found {len(new_games)} new games')
            with open(json_file_path, 'w') as f:
                ndjson.dump(new_games + json_games, f)
        return new_games + json_games


def process_json(games, username='kewko'):
    dates = []
    ratings = []
    daily_games = []
    for game in games:
        if game['players']['white']['user']['id'] == username:
            rating = game['players']['white']['rating']
        elif game['players']['black']['user']['id'] == username:
            rating = game['players']['black']['rating']
        else:
            continue
        created_time = game['createdAt']
        dates.append(datetime.fromtimestamp(created_time / 1000))
        ratings.append(rating)

    for date in dates:
        day_games = 0
        for date2 in dates:
            if date.date() == date2.date():
                day_games += 1
        daily_games.append(day_games)
    return [list(reversed(ratings)), list(reversed(daily_games))]

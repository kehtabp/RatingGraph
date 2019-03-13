import os
from datetime import datetime
from pathlib import Path

import ndjson
import requests


def get_json(username='kewko', game_mode="bullet", update=True, ensure_complete=False, maxnum=1000):
    json_file_path = f'data\lichess_{username}_{game_mode}.json'
    url = f'https://lichess.org/api/games/user/{username}'
    headers = {
        'Accept': 'application/x-ndjson'
    }
    parameters = {
        'rated': 'true',
        'perfType': game_mode,
        'max': maxnum
    }
    json_file = Path(json_file_path)
    if not json_file.is_file():
        print(f"File {json_file_path} not found, downloading...")
        r = requests.get(url, headers=headers, params=parameters)
        print(f"Download complete.")
        try:
            os.mkdir('data')
            print("data Directory Created ")
        except FileExistsError:
            pass

        with open(json_file_path, 'w') as f:
            json_games = ndjson.loads(r.text)
            ndjson.dump(json_games, f)
    else:
        with open(json_file, 'r') as file:
            json_games = ndjson.loads(file.read())

    if ensure_complete:
        until = json_games[-1]['createdAt']
        parameters['until'] = until
        old_games = True
        while old_games:
            until_date = datetime.fromtimestamp(until / 1000)
            print(f"Checking games before {until_date:%d/%m/%y %H:%M}...")
            r = requests.get(url, headers=headers, params=parameters)
            old_games = ndjson.loads(r.text)
            if old_games:
                until = old_games[-1]['createdAt']
                parameters['until'] = until
                print(f'Found {len(old_games)} older games.')
                json_games += old_games
                with open(json_file_path, 'a') as f:
                    f.write('\n')
                    ndjson.dump(old_games, f)
            else:
                print('No older games found')

    if not update:
        return json_games

    since = json_games[0]['createdAt']
    parameters['since'] = since
    del parameters['max']
    since_date = datetime.fromtimestamp(since / 1000)
    print(f"Checking games after {since_date:%d/%m/%y %H:%M}...")

    r = requests.get(url, headers=headers, params=parameters)
    new_games = ndjson.loads(r.content)
    if new_games:
        print(f'Found {len(new_games)} new games')
        with open(json_file_path, 'w') as f:
            ndjson.dump(new_games + json_games, f)
    else:
        print('No newer games found')

    return new_games + json_games

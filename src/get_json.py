import os
import time
from datetime import datetime
from pathlib import Path

import ndjson
import requests

try:
    from secrets import lichess_api_token
except ImportError:
    lichess_api_token = ''


def get(url):
    try:
        return requests.get(url)
    except Exception:
        # sleep for a bit in case that helps
        time.sleep(1)
        # try again
        return get(url)


def get_json(username='kewko', game_mode="bullet", update=True, ensure_complete=False, maxnum=1000, analysed=False):
    if analysed:
        json_file_path = f'data/analysed/lichess_{username}_{game_mode}.json'
    else:
        json_file_path = f'data/lichess_{username}_{game_mode}.json'

    url = f'https://webmin.kewko.win/tunnel/link.cgi/https://lichess.org/api/games/user/{username}'
    headers = {
        'Accept': 'application/x-ndjson',
        'Referer': 'https://webmin.kewko.win/tunnel/'
    }
    if lichess_api_token:
        headers['Authorization'] = f'Bearer {lichess_api_token}'
    parameters = {
        'rated': 'true',
        'perfType': game_mode,
        'max': maxnum,
        'analysed': analysed,
        'evals': analysed
    }
    json_file = Path(json_file_path)
    if not json_file.is_file():
        print(f"File {json_file_path} not found, downloading...")
        r = requests.get(url, headers=headers, params=parameters)
        print(r.request)
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
            t0 = time.time()
            try:
                r = requests.get(url, headers=headers, params=parameters)
                old_games = ndjson.loads(r.text)

            except Exception as x:
                t1 = time.time()
                print(f'It failed after: {t1-t0} with {x.__class__.__name__}')
            else:
                print('It eventually worked', r.status_code)
            finally:
                t2 = time.time()
                print('Took', t2 - t0, 'seconds')
            if len(old_games) > 0:
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

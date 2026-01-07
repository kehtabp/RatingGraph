#!/usr/bin/env python3
import json
import sys
import time

import requests

from utils import logger

try:
    from secrets import lichess_api_token
    logger.info("Loaded Lichess API token")
except ImportError:
    lichess_api_token = ''

REQUEST_TIMEOUT = 30


def get_unanalysed_game(username, skip=0, count=False):
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
        params['max'] = skip + 1

    r = requests.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
    if count:
        return len(r.text.split())
    return json.loads(r.text.split()[-1])['id']


def analyse(game_id, cookie):
    headers = {
        'Cookie': cookie
    }
    url = f'https://lichess.org/{game_id}/request-analysis'
    logger.info(f'Analyzing {game_id}...')

    r = requests.post(url, headers=headers, timeout=REQUEST_TIMEOUT)
    if r.status_code != 204:
        raise Exception(f"Analysis request failed with status {r.status_code}: {r.text}")


def main():
    if len(sys.argv) < 2:
        logger.error("Usage: python analyse.py <cookie> [username]")
        sys.exit(1)

    cookie = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else 'kewko'

    prev_game_id = 0
    games_analysed = 0
    skip = 0

    while True:
        game_id = get_unanalysed_game(username, skip=skip)
        if game_id != prev_game_id:
            try:
                analyse(game_id, cookie)
                games_analysed += 1
            except Exception as e:
                if skip > 4 or games_analysed >= 30:
                    remaining = get_unanalysed_game(username, count=True)
                    logger.info(f"Done. Analysed {games_analysed} games. {remaining} games remaining.")
                    break
                else:
                    logger.warning(f"Error: {e}. Skipping {game_id}")
                    skip += 1
        else:
            logger.debug("Waiting for analysis to complete...")
        time.sleep(5)
        prev_game_id = game_id


if __name__ == '__main__':
    main()

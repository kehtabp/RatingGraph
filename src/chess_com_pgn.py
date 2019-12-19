import os
import sys
from datetime import datetime
from pathlib import Path
import requests


def get_full_pgn(username):
    if len(sys.argv) > 1:
        prefix = sys.argv[1] + 'link.cgi/'
        request_headers = {'referer': sys.argv[1]}
    else:
        prefix = ''
        request_headers = {}
    base_url = prefix + "https://api.chess.com/pub/player/" + username + "/games/"
    archives_url = base_url + "archives"
    full_pgn = ""
    # read the archives url and store in a list
    f = requests.get(archives_url, headers=request_headers)
    archives_list = f.json()['archives']
    for archive in archives_list:
        info = archive[12:].split('/')
        file_path = f'data/{info[0]}/{info[3]}/{info[5]}-{info[6]}.pgn'
        pgn_file = Path(file_path)
        if not pgn_file.is_file():
            print(f'Downloading {file_path}')
            os.makedirs(os.path.dirname(pgn_file), exist_ok=True)
            url = prefix + archive + "/pgn"
            pgn = requests.get(url, headers=request_headers).text
            full_pgn += pgn
            with open(pgn_file, 'w', encoding="utf-8") as file:
                file.writelines(pgn)
        else:
            with open(pgn_file, 'r') as file:
                print(f'Reading {file_path}')
                try:
                    full_pgn += file.read()
                except UnicodeDecodeError as error:
                    print(error)

    return full_pgn


def detect_adoption(username: str, pgn: str, child=True) -> list:
    opponent = ''
    date = ''
    children = []
    games_text = pgn.split('\n\n')
    consecutive_wins: int = 0
    previous_opponent = ''
    for gameText in enumerate(games_text):
        headers = gameText.split('\n')
        for header in headers:
            title_value = header.split(' "')
            if len(title_value) == 2:
                title = title_value[0][1:]
                value = title_value[1][:-2]
                if title == 'Black' or title == 'White':
                    if value != username:
                        opponent = value
                if title == 'UTCDate':
                    date = value
                if title == 'Termination' and child:
                    if username + ' won' not in value:
                        consecutive_wins = 0
                        # print(value)
                    else:
                        if opponent == previous_opponent:
                            consecutive_wins += 1
                            if consecutive_wins >= 10:
                                consecutive_wins = 0
                                print(username + ' adopted ' +
                                      opponent + ' on ' + date)
                                children.append(opponent)
                        else:
                            consecutive_wins = 0
                        previous_opponent = opponent
                # else if opp TODO adoptive parents
    return children

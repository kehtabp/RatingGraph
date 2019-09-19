import sys
from datetime import datetime
from pathlib import Path
from urllib import request

from dateutil import parser


def process_pgn(username, game_mode):
    text = get_pgn(username)
    games_text = text.split('\n\n\n')
    games = []
    for index, gameText in enumerate(games_text):
        # if index == 100:
        #     break
        headers = gameText.split('\n')
        game = {}
        for header in headers:
            title_value = header.split(' "')
            if len(title_value) == 2:
                title = title_value[0][1:]
                value = title_value[1][:-2]
                game[title] = value
                if value == username:
                    game['Side'] = title
                if title == 'UTCTime':
                    game['Timestamp'] = parser.parse(game['UTCDate'] + ' ' + value)
            elif len(header) > 1:
                game['PGN'] = header
        if game.get('Event') == ('Rated %s game' % game_mode):
            games.append(game)
    ratings = []
    dates = []
    daily_games = []
    for game in games:
        timestamp = game['Timestamp']
        rating = int(game[game['Side'] + 'Elo'])
        dates.append(timestamp)
        ratings.append(rating)
    for date in dates:
        day_games = 0
        for date2 in dates:
            if date.date() == date2.date():
                day_games += 1
        daily_games.append(day_games)

    return [list(reversed(ratings)), list(reversed(daily_games))]


def get_pgn(username):
    today = datetime.now()
    pgn_file_path = f'data/lichess_{username}_{today:%Y-%m-%d}.pgn'
    url = f'https://lichess.org/games/export/{username}'
    pgn_file = Path(pgn_file_path)
    if not pgn_file.is_file():
        request.urlretrieve(url, pgn_file_path, reporthook)
    with open(pgn_file, 'r') as file:
        return file.read()


def reporthook(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(total_size)), read_so_far, total_size)
        sys.stderr.write(s)
        if read_so_far >= total_size:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (read_so_far,))

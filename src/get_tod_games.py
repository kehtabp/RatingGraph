from datetime import datetime
from pprint import pprint

from src.get_json import get_json

json = get_json(game_mode='blitz', update=False)


def win_rate(games, username='kewko'):
    hours = list(range(24))
    win_rates = []
    wins = [0] * 24
    losses = [0] * 24
    draws = [0] * 24
    game_num = [0] * 24
    for game in games:
        created_time = game['createdAt']
        game_time = datetime.fromtimestamp(created_time / 1000)
        game_time_hour = game_time.hour
        game_num[game_time_hour] += 1
        if 'winner' in game:
            if game['players'][game['winner']]['user']['name'] == username:
                wins[game_time_hour] += 1
            else:
                losses[game_time_hour] += 1
        else:
            draws[game_time_hour] += 1

    for hour in hours:
        win_rates.append(wins[hour] / game_num[hour])
    return [win_rates, game_num]


pprint(win_rate(json))

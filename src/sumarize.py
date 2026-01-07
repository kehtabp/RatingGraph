from datetime import datetime

import numpy as np

from get_json import get_json
from utils import is_black, get_color, logger


def game_results(analyzed_games, username):
    acpls = []
    for game in analyzed_games:
        side = get_color(game, username)
        timestamp = int(game['createdAt']) / 1000
        game_date = datetime.fromtimestamp(timestamp)

        if 'analysis' in game['players'][side]:
            acpls.append([game_date, game['players'][side]['analysis']['acpl']])

    return acpls


def summarise(analyzed_games, username):
    top_moves = {}
    for game in analyzed_games:
        black = is_black(game, username)
        moves = game['moves'].split(' ')
        user_moves = moves[black::2]

        if 'analysis' not in game:
            continue

        eval_changes = []
        previous_evaluation = None
        for i, analysis in enumerate(game['analysis']):
            try:
                evaluation = analysis['eval']
            except KeyError:
                king_eval = 30000
                mate = analysis['mate']
                if mate < 0:
                    king_eval *= -1
                if mate > 8:
                    mate = 8
                elif mate < -8:
                    mate = -8
                evaluation = king_eval - (mate * 1000)

            if black:
                evaluation *= -1
            if evaluation > 1000:
                evaluation = 1000
            if evaluation < -1000:
                evaluation = -1000
            if previous_evaluation is None:
                previous_evaluation = evaluation
            eval_change = evaluation - previous_evaluation
            eval_changes.append(eval_change)
            previous_evaluation = evaluation

        user_eval_changes = eval_changes[black::2]
        for index, move in enumerate(user_moves):
            try:
                top_moves[move]['freq'] += 1
                top_moves[move]['eval_change'].append(user_eval_changes[index])
            except KeyError:
                try:
                    top_moves[move] = {'freq': 1, 'eval_change': [user_eval_changes[index]]}
                except IndexError:
                    pass
            except IndexError:
                pass
    return top_moves


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


if __name__ == '__main__':
    username = 'kewko'
    games = get_json(analysed='yes')
    results = game_results(games, username)
    for result in results:
        logger.info(f'{result[0]}\t{result[1]}')

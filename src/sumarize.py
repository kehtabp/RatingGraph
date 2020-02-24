from datetime import datetime

import numpy as np

from get_json import get_json
from get_moves import user_side


def game_results(analyzed_games):
    acpls = []
    for game in analyzed_games:
        black = user_side(game, 'kewko')
        if black:
            side = 'black'
        else:
            side = 'white'

        timestamp = int(game['createdAt']) / 1000
        game_date = datetime.fromtimestamp(timestamp)

        acpls.append([game_date, game['players'][side]['analysis']['acpl']])

    return acpls


def summarise(analyzed_games):
    top_moves = {}
    for game in analyzed_games:
        black = user_side(game, 'kewko')
        # pprint(analyzed_games)
        moves = game['moves'].split(' ')
        user_moves = moves[black::2]

        eval_changes = []
        previous_evaluation = None
        for i, analysis in enumerate(game['analysis']):

            try:
                evaluation = analysis['eval']
            except KeyError:
                # continue
                king_eval = 30000
                mate = analysis['mate']
                if mate < 0:
                    king_eval *= -1
                if mate > 8:
                    mate = 8
                elif mate < -8:
                    mate = -8
                evaluation = king_eval - (mate * 1000)

                # print(f"Eval is mate in {analysis['mate']}. Assigning {evaluation}")

            if black:
                evaluation *= - 1
            if evaluation > 1000:
                evaluation = 1000
            if evaluation < -1000:
                evaluation = -1000
            if previous_evaluation is None:
                previous_evaluation = evaluation
            eval_change = evaluation - previous_evaluation
            eval_changes.append(eval_change)
            white_move = i % 2 == 0
            my_move = white_move ^ black

            # if eval_change > 0 and my_move:
            #     print(f"{game['id']}\t{i}.{moves[i]}\t{eval_change}\t{analysis}.")

            # print(f'{index}. {evaluation} Change:{eval_change}')
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
                # print("Eval not there")
    return top_moves


games = get_json(analysed='yes')


# summary = summarise(games)
# with open('data\\summary.csv', 'w') as f:
#     for move_sum in summary:
#         average_eval_change = numpy.average(summary[move_sum]['eval_change'])
#         summary[move_sum]['average_change'] = average_eval_change
#         f.write(f'{move_sum},{summary[move_sum]["freq"]},{average_eval_change},{summary[move_sum]["eval_change"]}\n')

# summary = {k: v for k, v in sorted(summary.items(), key=lambda item: item[1]['average_change'])}
# print(summary)
def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


results = game_results(games)
# average = moving_average(results, n=100)
for result in results:
    print(f'{result[0]}\t{result[1]}')
print()

from datetime import datetime

from get_json import get_json


def get_blunders(username, games=None, before_move=10, step=5):
    blunder_counter = 0
    blunder_list = []
    if games is None:
        games = get_json('kewko', 'blitz', update=True, analysed=True)
    for game in games:
        black = is_black(game, username)
        created_time = game['createdAt']
        game_time = datetime.fromtimestamp(created_time / 1000)
        for i, evaluation in enumerate(game['analysis'][black::2]):
            try:
                if evaluation['judgment']['name'] == 'Blunder' and i <= before_move and i > before_move - step:
                    blunder_counter += 1
                    moves = game['moves'].split(' ')
                    move_number = (i + 1) * 2 + black - 1
                    print(
                        f"{game_time:%c}\thttps://lichess.org/{game['id']}{get_color(game, username)}#{move_number:<3}"
                        f"{'      ' if not black else ''}\t with {moves[move_number - 1]:<4} instead of "
                        f"{evaluation['best']:<4} on move {move_number}")
                    break
            except KeyError:
                continue
    print(f"Blundered in {blunder_counter}/{len(games)} games between moves {before_move - step} and {before_move}.")


def is_black(game, username):
    if game['players']['black']['user']['name'].casefold() == username.casefold():
        black = True
    elif game['players']['white']['user']['name'].casefold() == username.casefold():
        black = False
    else:
        raise Exception("User didn't play")
    return black


def get_color(game, username):
    if (is_black(game, username)):
        return '/black'
    else:
        return ''


g_games = get_json('kewko', 'blitz', update=True, analysed=True)
g_step = 10
for i in range(10, 150, g_step):
    get_blunders('kewko', before_move=i, games=g_games, step=g_step)

from datetime import datetime

from get_json import get_json
from utils import is_black, get_color_url_suffix, logger


def get_blunders(username, games=None, before_move=10, step=5):
    blunder_counter = 0
    if games is None:
        games = get_json(username, 'blitz', update=True, analysed=True)
    for game in games:
        black = is_black(game, username)
        created_time = game['createdAt']
        game_time = datetime.fromtimestamp(created_time / 1000)
        if 'analysis' not in game:
            continue
        for i, evaluation in enumerate(game['analysis'][black::2]):
            try:
                if evaluation['judgment']['name'] == 'Blunder' and i <= before_move and i > before_move - step:
                    blunder_counter += 1
                    moves = game['moves'].split(' ')
                    move_number = (i + 1) * 2 + black - 1
                    logger.info(
                        f"{game_time:%c}\thttps://lichess.org/{game['id']}{get_color_url_suffix(game, username)}#{move_number:<3}"
                        f"{'      ' if not black else ''}\t with {moves[move_number - 1]:<4} instead of "
                        f"{evaluation['best']:<4} on move {move_number}")
                    break
            except KeyError:
                continue
    logger.info(f"Blundered in {blunder_counter}/{len(games)} games between moves {before_move - step} and {before_move}.")


if __name__ == '__main__':
    g_games = get_json('kewko', 'blitz', update=True, analysed=True)
    g_step = 10
    for i in range(10, 150, g_step):
        get_blunders('kewko', before_move=i, games=g_games, step=g_step)

import re
from pprint import pprint

from get_json import get_json
from utils import is_black, get_color, logger


def get_moves(username, games=None, piece='N', takes=False):
    if games is None:
        games = get_json(username, 'blitz', update=False, analysed=True)
    logger.info(f"Getting moves for {piece}")
    board = [[0] * 8 for _ in range(8)]
    regex = re.compile(
        '(?P<piece>[KQRNB])?(?P<specifier>[a-h1-8])?(?P<takes>x)?(?P<position>[a-h][1-8])(?P<action>[#+])?')
    # Ignores castles|(?P<castles>O-O|O-O-O)
    for game in games:
        moves = game['moves'].split(' ')
        black = is_black(game, username)

        for i, move in enumerate(moves):
            if (i % 2 == 0 and not black) or (i % 2 != 0 and black):
                move = re.search(regex, move)
                if move and move['piece'] == piece:
                    if takes:
                        if not move['takes']:
                            break
                    position = move['position']
                    file = ord(position[:1]) - 97
                    rank = int(position[1:]) - 1
                    board[rank][file] += 1
    return board


if __name__ == '__main__':
    pprint(list(reversed(get_moves('kewko'))))

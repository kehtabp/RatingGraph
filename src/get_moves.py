import re
from pprint import pprint

from src.get_json import get_json

json = get_json('kewko', 'blitz', True)


def get_moves(username, games, piece):
    print(f"Getting moves for {piece}")
    board = [[0] * 8, [0] * 8, [0] * 8, [0] * 8, [0] * 8, [0] * 8, [0] * 8, [0] * 8]
    regex = re.compile(
        '(?P<piece>[KQRNB])?(?P<specifier>[a-h1-8])?(?P<takes>x)?(?P<position>[a-h][1-8])(?P<action>[#?+])?')
    # Ignores castles|(?P<castles>O-O|O-O-O)
    for game in games:
        moves = game['moves'].split(' ')
        if game['players']['white']['user']['name'].casefold() == username.casefold():
            white = True
        elif game['players']['black']['user']['name'].casefold() == username.casefold():
            white = False
        else:
            raise Exception("User didn't play")

        for i, move in enumerate(moves):
            if (i % 2 == 0 and white) or (i % 2 != 0 and not white):
                move_object = re.search(regex, move)
                if move_object and move_object['piece'] == piece:
                    position = move_object['position']
                    file = ord(position[:1]) - 97
                    rank = int(position[1:]) - 1
                    # print(f'{move_object["piece"]} moved to {move_object["position"]}')
                    board[rank][file] += 1
    return board


pprint(list(reversed(get_moves('kewko', json, 'N'))))

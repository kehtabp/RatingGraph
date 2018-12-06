from dateutil import parser


def process_pgn(username, game_mode):
    pgn_path = 'C:\\Users\\aleksandrovk\\Downloads\\lichess_%s_2018-12-06.pgn' % username
    file = open(pgn_path, 'r')
    text = file.read()
    games_text = text.split('\n\n\n')
    games = []
    for index, gameText in enumerate(games_text):
        # if index == 100:
        #     break
        headers = gameText.split('\n')
        game = {}
        add_game = False
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
    for game in games:
        timestamp = game['Timestamp']
        rating = int(game[game['Side'] + 'Elo'])
        dates.append(timestamp)
        ratings.append(rating)
    return [ratings, dates]

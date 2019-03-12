from get_json import get_json
from get_ratings import ratings_dailygames
from plot_rating import plot_rating

newlines = []
with open('data\queue', 'r') as f:
    for line in f.readlines():
        if len(line.split(',')) == 3:
            username, game_mode, url = line.strip().split(',')
        else:
            username, game_mode = line.strip().split(',')

            json = get_json(username, game_mode, update=True)
            ratings, daily_games = ratings_dailygames(json, username, 1000)
            url = plot_rating(ratings, daily_games, username, game_mode=game_mode, size='large', export_video=True,
                              show_graph=False,
                              upload=True)
        newlines.append(f"{username},{game_mode},{url}\n")
with open('data\queue', 'w') as f:
    f.writelines(newlines)

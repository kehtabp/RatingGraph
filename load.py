from get_json import get_json
from plot_graph import plot_graph
from process_json import process_json

newlines = []
with open('data\queue', 'r') as f:
    for line in f.readlines():
        if len(line.split(',')) == 3:
            username, game_mode, url = line.strip().split(',')
        else:
            username, game_mode = line.strip().split(',')

            json = get_json(username, game_mode, update=False)
            ratings, daily_games = process_json(json, username)
            url = plot_graph(ratings, daily_games, username, game_mode=game_mode, size='large', export_video=True,
                             show_graph=False,
                             upload=True)
        newlines.append(f"{username},{game_mode},{url}\n")
with open('data\queue', 'w') as f:
    f.writelines(newlines)

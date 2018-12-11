from get_json import get_json
from plot_graph import plot_graph
from process_json import process_json

GAME_MODE = 'bullet'
USERNAME = 'kewko'

json = get_json(USERNAME, GAME_MODE, update=False)
ratings, daily_games = process_json(json, USERNAME)
plot_graph(ratings, daily_games, USERNAME, size='b', export_video=False)

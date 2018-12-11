from plot_graph import plot_graph
from process_json import process_json, get_json

GAME_MODE = 'blitz'
USERNAME = 'kewko'

json = get_json(USERNAME, 'blitz')
ratings, daily_games = process_json(json, USERNAME)
plot_graph(ratings, daily_games, USERNAME, size='small', export_video=False)

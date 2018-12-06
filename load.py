from plot_graph import plot_graph
from process_pgn import process_pgn

GAME_MODE = 'Blitz'
USERNAME = 'kewko'

ratings, daily_games = process_pgn(USERNAME, GAME_MODE)

plot_graph(ratings, daily_games, USERNAME, size='big', export_video=True)

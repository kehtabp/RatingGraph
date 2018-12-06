from plot_graph import plot_graph
from process_pgn import process_pgn

GAME_MODE = 'Blitz'
USERNAME = 'kewko'

ratings, dates = process_pgn(USERNAME, GAME_MODE)

plot_graph(ratings, dates, USERNAME)

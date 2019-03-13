import argparse

from get_json import get_json
from get_ratings import ratings_dailygames
from plot_rating import plot_rating

parser = argparse.ArgumentParser(description='Generate graph for Lichess ')
username_source = parser.add_mutually_exclusive_group(required=True)
username_source.add_argument('--file',
                             action='store_true',
                             default=False,
                             dest='file',
                             help='Pass to load usernames and game modes from data\queue.csv')
username_source.add_argument('-u', '--username',
                             action='store',
                             dest='username',
                             help='Pass to make graph for a single username/game mode')

parser.add_argument('-e', '--export_video',
                    action='store_true',
                    default=False,
                    dest='export',
                    help='''Export video to ./export/ChessGraph_USERNAME_GAMEMODE_SIZE.mp4.
                         !If this is not passed graph will be displayed in the UI Window!''')
parser.add_argument('--upload_video',
                    action='store_true',
                    default=False,
                    dest='upload',
                    help='Upload to Streamable ./secrets.py needs to contain stramable_username and stramable_password')

parser.add_argument('-n', '--num',
                    action='store',
                    default=1000,
                    dest='NUMBER_OF_GAMES',
                    help="Number of games to show on graph. (0 for all games)",
                    type=int)
parser.add_argument('-m', '--mode',
                    action='store',
                    default='blitz',
                    dest='game_mode',
                    help="Game mode (bullet/blitz/classical)")
parser.add_argument('-b', '--big',
                    action='store_true',
                    default=False,
                    dest='big',
                    help="Generate big chart, Defaults to smaller resolution")
parser.add_argument('--noupdate',
                    action='store_false',
                    default=True,
                    dest='UPDATE',
                    help="Pass to create graph from existing data only")

args = parser.parse_args()
game_mode = args.game_mode
UPDATE = args.UPDATE
NUMBER_OF_GAMES = args.NUMBER_OF_GAMES

newlines = []
if args.file:
    with open('data\queue.csv', 'r') as f:
        for line in f.readlines():
            if len(line.split(',')) == 3:
                username, game_mode, url = line.strip().split(',')
            else:
                username, game_mode = line.strip().split(',')

                json = get_json(username, game_mode, UPDATE, maxnum=NUMBER_OF_GAMES)
                ratings, daily_games = ratings_dailygames(json, username, NUMBER_OF_GAMES)
                url = plot_rating(ratings, daily_games, username, game_mode=game_mode, big=args.big,
                                  export_video=args.export,
                                  show_graph=not args.export,
                                  upload=args.upload)
            newlines.append(f"{username},{game_mode},{url}\n")
    with open('data\queue.csv', 'w') as f:
        f.writelines(newlines)
else:
    username = args.username
    json = get_json(username, game_mode, UPDATE, maxnum=NUMBER_OF_GAMES)
    ratings, daily_games = ratings_dailygames(json, username, NUMBER_OF_GAMES)
    url = plot_rating(ratings, daily_games, username, game_mode=game_mode, big=args.big,
                      export_video=args.export,
                      show_graph=not args.export,
                      upload=args.upload)

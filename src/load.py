#!/usr/bin/env python3
import argparse
import csv

from get_json import get_json
from get_ratings import ratings_dailygames
from plot_rating import plot_rating

parser = argparse.ArgumentParser(description='Generate graph for Lichess ')
username_source = parser.add_mutually_exclusive_group(required=True)
username_source.add_argument('--file',
                             action='store_true',
                             default=False,
                             dest='file',
                             help='Pass to load usernames and game modes from ./queue.csv')
username_source.add_argument('-u', '--username',
                             action='store',
                             dest='username',
                             help='Pass to make graph for a single username/game mode')

parser.add_argument('-e', '--export_video',
                    action='store_true',
                    default=False,
                    dest='export',
                    help='Export video to ./export/ChessGraph_USERNAME_GAMEMODE_SIZE.mp4. ')
parser.add_argument('--show',
                    action='store_true',
                    default=False,
                    dest='show',
                    help='Show video. Window manager is required.')
parser.add_argument('--upload_video',
                    action='store_true',
                    default=False,
                    dest='upload',
                    help='Upload to Streamable ./secrets.py needs to contain streamable_username and '
                         'streamable_password')

parser.add_argument('-n', '--num',
                    action='store',
                    default=1000,
                    dest='number_of_games',
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
                    dest='update',
                    help="Pass to create graph from existing data only")
parser.add_argument('--ensurecomplete',
                    action='store_true',
                    default=False,
                    dest='ensure',
                    help="Pass to create graph from existing data only")


args = parser.parse_args()
GAME_MODE = args.game_mode
UPDATE = args.update
NUMBER_OF_GAMES = args.number_of_games
UPLOAD = args.upload
EXPORT_VIDEO = args.export
SHOW_VIDEO = args.show
ENSURE_COMPLETE = args.ensure
BIG = args.big

newlines = []

if args.file:
    args.upload = True
    queue_csv = 'data/queue.csv'
    lines = []
    with open(queue_csv, 'r') as f:
        csv_reader = csv.DictReader(f)
        for line in csv_reader:
            if not line['Url']:
                username = line['Username']
                game_mode = line['Game mode']

                json = get_json(username, game_mode, UPDATE, maxnum=NUMBER_OF_GAMES)
                if SHOW_VIDEO or EXPORT_VIDEO:
                    ratings, daily_games = ratings_dailygames(json, username, NUMBER_OF_GAMES)
                    line['Url'] = plot_rating(ratings, daily_games, username, game_mode=game_mode, big=BIG,
                                              export_video=EXPORT_VIDEO,
                                              show_graph=SHOW_VIDEO,
                                              upload=UPLOAD)
                    lines.append(line)
        with open(queue_csv, 'w', newline='') as fw:
            writer = csv.DictWriter(fw, csv_reader.fieldnames, dialect=csv_reader.dialect)
            writer.writeheader()
            writer.writerows(lines)
else:
    username = args.username
    json = get_json(username, GAME_MODE, UPDATE, maxnum=NUMBER_OF_GAMES, ensure_complete=ENSURE_COMPLETE)
    if SHOW_VIDEO or EXPORT_VIDEO:
        ratings, daily_games = ratings_dailygames(json, username, NUMBER_OF_GAMES)
        url = plot_rating(ratings, daily_games, username, game_mode=GAME_MODE, big=BIG,
                          export_video=EXPORT_VIDEO,
                          show_graph=SHOW_VIDEO,
                          upload=UPLOAD)

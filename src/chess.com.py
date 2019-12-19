import os
import sys
from datetime import datetime
from pathlib import Path
import requests
import json

def detect_json_adoption(username, json):
    consecutive_wins: int = 0
    previous_opponent = ''
    for game in json:
        if game['white']['username'] == username:
            our_color = 'white'
            opponent_color = 'black'
        else:
            our_color = 'black'
            opponent_color = 'white'

        opponent = game[opponent_color]['username']  # record opp name
        if game[our_color]['result'] == 'win':  # we win
            if opponent == previous_opponent:
                consecutive_wins += 1
                if consecutive_wins == 10:
                    consecutive_wins = 0
                    date = datetime.fromtimestamp(game["end_time"])
                    print(
                        f'{opponent} was adopted by {username} on {date}\n\tRating: {game[opponent_color]["rating"]}')
            else:
                consecutive_wins = 0
        else:
            consecutive_wins = 0
        previous_opponent = opponent


def get_month_games(username, month):
    url = f'https://api.chess.com/pub/player/{username}/games/{month}'
    return requests.get(url).json()['games']


def get_all_games(username):
    url = f'https://api.chess.com/pub/player/{username}/games/archives'
    archives = requests.get(url).json()['archives']
    all_games = []
    for month in archives:
        games =requests.get(month).json()['games']
        all_games +=games
    return all_games

un="ChessBrah"
detect_json_adoption(un, get_all_games(un))
# detect_json_adoption(un, get_month_games(un, "2019/01"))

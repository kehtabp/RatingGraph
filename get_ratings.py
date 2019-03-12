import itertools
from datetime import datetime


def ratings_dailygames(games, username='kewko', number=0):
    dates = []
    ratings = []
    daily_games = []
    for game in itertools.islice(games, 0, number):
        if game['players']['white']['user']['name'] == username:
            rating = game['players']['white']['rating']
        elif game['players']['black']['user']['name'] == username:
            rating = game['players']['black']['rating']
        else:
            continue
        created_time = game['createdAt']
        dates.append(datetime.fromtimestamp(created_time / 1000))
        ratings.append(rating)

    for date in dates:
        day_games = 0
        for date2 in dates:
            if date.date() == date2.date():
                day_games += 1
        daily_games.append(day_games)
    return [list(reversed(ratings)), list(reversed(daily_games))]

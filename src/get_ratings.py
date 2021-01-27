import itertools
from datetime import datetime, timedelta

from get_moves import get_color


def ratings_daily_games(games, username='kewko', number=None):
    dates = []
    ratings = []
    daily_games = []
    weekly_games = {}

    for game in itertools.islice(games, 0, number):
        color = get_color(game, username)
        rating = game['players'][color]['rating']
        rating_diff = game['players'][color]['ratingDiff']
        old_rating = rating + rating_diff

        last_move_time = datetime.fromtimestamp(game['lastMoveAt'] / 1000)
        created_time = datetime.fromtimestamp(game['createdAt'] / 1000)

        week_number = created_time.strftime("%Y-%W")
        try:
            weekly_games[week_number]['games'] += 1
        except KeyError:
            start = created_time - timedelta(days=created_time.weekday(),
                                             minutes=created_time.minute, hours=created_time.hour)
            weekly_games[week_number] = {'games': 1, 'week_start': start}
        dates.append(last_move_time)
        dates.append(created_time)

        ratings.append(rating)
        ratings.append(old_rating)
    wg = []
    wgt = []
    for week in weekly_games:
        wg.append(weekly_games[week]['games'])
        wgt.append(weekly_games[week]['week_start'])
    for date in dates:
        day_games = 0
        for date2 in dates:
            if date.date() == date2.date():
                day_games += 1
        daily_games.append(day_games)
    return {'ratings': list(reversed(ratings)), 'daily_games': list(reversed(daily_games)),
            'dates': list(reversed(dates)), 'weekly_games': list(reversed(wg)),
            'weekly_starts': list(reversed(wgt))}

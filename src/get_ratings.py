import itertools
from datetime import datetime, timedelta

from utils import get_color, count_daily_games, logger


def ratings_daily_games(games, username='kewko', number=None):
    dates = []
    ratings = []
    weekly_games = {}
    skipped = 0

    # number=0 means all games (same as None)
    limit = number if number and number > 0 else None
    for game in itertools.islice(games, 0, limit):
        color = get_color(game, username)
        rating = game['players'][color]['rating']
        if 'ratingDiff' not in game['players'][color]:
            skipped += 1
            continue
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

    # O(n) daily game counting using Counter (was O(n²))
    daily_games = count_daily_games(dates)

    total_processed = len(ratings) // 2  # Each game adds 2 rating points
    logger.info(f"Processed {total_processed} games with rating data (skipped {skipped} without ratingDiff)")

    if not ratings:
        logger.warning("No games with rating data found!")

    return {'ratings': list(reversed(ratings)), 'daily_games': list(reversed(daily_games)),
            'dates': list(reversed(dates)), 'weekly_games': list(reversed(wg)),
            'weekly_starts': list(reversed(wgt))}

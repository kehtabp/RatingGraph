"""Shared utility functions for RatingGraph."""

import logging
from collections import Counter
from datetime import datetime
from typing import List, Dict, Any

# Configure logging for the package
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('ratinggraph')


def is_black(game: Dict[str, Any], username: str) -> bool:
    """Check if the user played as black in a game.

    Args:
        game: Game data dictionary from Lichess API
        username: Player's username

    Returns:
        True if user played as black, False if white

    Raises:
        ValueError: If user didn't play in the game
    """
    black_name = game['players']['black']['user']['name'].casefold()
    white_name = game['players']['white']['user']['name'].casefold()
    username_lower = username.casefold()

    if black_name == username_lower:
        return True
    elif white_name == username_lower:
        return False
    else:
        raise ValueError(f"User '{username}' didn't play in this game")


def get_color(game: Dict[str, Any], username: str) -> str:
    """Get the color the user played as in a game.

    Args:
        game: Game data dictionary from Lichess API
        username: Player's username

    Returns:
        'black' or 'white'
    """
    return 'black' if is_black(game, username) else 'white'


def get_color_url_suffix(game: Dict[str, Any], username: str) -> str:
    """Get the URL suffix for the user's color perspective.

    Args:
        game: Game data dictionary from Lichess API
        username: Player's username

    Returns:
        '/black' if user played black, empty string otherwise
    """
    return '/black' if is_black(game, username) else ''


def count_daily_games(dates: List[datetime]) -> List[int]:
    """Count number of games played per day for each date in the list.

    This is an O(n) implementation using Counter, replacing the previous
    O(n²) nested loop approach.

    Args:
        dates: List of datetime objects for each game

    Returns:
        List of game counts where each entry corresponds to games played
        on that date's calendar day
    """
    # Count games per calendar day - O(n)
    date_counts = Counter(d.date() for d in dates)
    # Map back to original list - O(n)
    return [date_counts[d.date()] for d in dates]

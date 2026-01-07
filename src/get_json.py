import os
import shutil
import tempfile
import time
from datetime import datetime
from pathlib import Path

import ndjson
import requests

from utils import logger

try:
    from secrets import lichess_api_token
except ImportError:
    lichess_api_token = ''

# Connection settings
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 5
RETRY_BACKOFF_BASE = 2  # exponential backoff base

# Create a session for connection pooling
_session = None


def get_session():
    """Get or create a requests session for connection pooling."""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update({
            'Accept': 'application/x-ndjson',
        })
    return _session


def get_json(username='kewko', game_mode="blitz", update=False, ensure_complete=False, maxnum=1000, analysed=None,
             prefix=''):
    if analysed:
        json_file_path = f'data/analysed/lichess_{username}_{game_mode}.json'
    else:
        json_file_path = f'data/lichess_{username}_{game_mode}.json'

    url = f'{prefix}https://lichess.org/api/games/user/{username}'
    headers = {
        'Accept': 'application/x-ndjson',
        'Referer': prefix
    }
    if lichess_api_token:
        headers['Authorization'] = f'Bearer {lichess_api_token}'
    parameters = {
        'rated': 'true',
        'perfType': game_mode,
    }
    # Only set max if specified and > 0 (0 means all games)
    if maxnum and maxnum > 0:
        parameters['max'] = maxnum

    if analysed:
        parameters['evals'] = analysed
        parameters['analysed'] = analysed

    json_file = Path(json_file_path)
    if not json_file.is_file():
        if maxnum and maxnum > 0:
            logger.info(f"File {json_file_path} not found, downloading up to {maxnum} games...")
        else:
            logger.info(f"File {json_file_path} not found, downloading all games...")
        r = get_with_retry(url, headers=headers, params=parameters)
        logger.debug(f"Request URL: {r.request.url}")
        json_games = ndjson.loads(r.text)
        logger.info(f"Download complete. Got {len(json_games)} games.")
        try:
            os.makedirs('data', exist_ok=True)
            if analysed:
                os.makedirs('data/analysed', exist_ok=True)
        except OSError as e:
            logger.error(f"Failed to create data directory: {e}")
            raise

        atomic_write_json(json_file_path, json_games)
    else:
        with open(json_file, 'r') as file:
            json_games = ndjson.loads(file.read())
        logger.info(f"Loaded {len(json_games)} games from cache.")

    if ensure_complete and json_games:
        # Use a reasonable batch size for pagination when fetching older games
        batch_size = maxnum if (maxnum and maxnum > 0) else 500
        parameters['max'] = batch_size
        until = json_games[-1]['createdAt']
        parameters['until'] = until
        old_games = True
        total_old_games = 0
        while old_games:
            until_date = datetime.fromtimestamp(until / 1000)
            logger.info(f"Checking games before {until_date:%d/%m/%y %H:%M}...")
            t0 = time.time()
            try:
                r = get_with_retry(url, headers=headers, params=parameters)
                old_games = ndjson.loads(r.text)
            except Exception as e:
                t1 = time.time()
                logger.error(f'Request failed after: {t1 - t0:.2f}s with {e.__class__.__name__}: {e}')
                raise
            else:
                logger.debug(f'Request succeeded with status {r.status_code}')
            finally:
                t2 = time.time()
                logger.debug(f'Request took {t2 - t0:.2f} seconds')

            if len(old_games) > 0:
                until = old_games[-1]['createdAt']
                parameters['until'] = until
                total_old_games += len(old_games)
                logger.info(f'Found {len(old_games)} older games (total: {total_old_games}).')
                json_games += old_games
                # Append to file
                with open(json_file_path, 'a') as f:
                    f.write('\n')
                    ndjson.dump(old_games, f)
            else:
                logger.info(f'No older games found. Total games: {len(json_games)}')

    if not update:
        return json_games

    since = json_games[0]['createdAt']
    parameters['since'] = since
    parameters.pop('max', None)  # Remove max if present (may not exist if maxnum=0)
    since_date = datetime.fromtimestamp(since / 1000)
    logger.info(f"Checking games after {since_date:%d/%m/%y %H:%M}...")

    r = get_with_retry(url, headers=headers, params=parameters)
    new_games = ndjson.loads(r.content)
    if new_games:
        logger.info(f'Found {len(new_games)} new games')
        # Use atomic write to prevent data loss
        atomic_write_json(json_file_path, new_games + json_games)
    else:
        logger.info('No newer games found')

    return new_games + json_games


def atomic_write_json(file_path, data):
    """Write JSON data to file atomically using a temp file and rename.

    This prevents data loss if the process is interrupted during write.
    """
    dir_path = os.path.dirname(file_path) or '.'
    fd, temp_path = tempfile.mkstemp(dir=dir_path, suffix='.json.tmp')
    try:
        with os.fdopen(fd, 'w') as f:
            ndjson.dump(data, f)
        shutil.move(temp_path, file_path)
        logger.debug(f'Atomically wrote {len(data)} games to {file_path}')
    except Exception:
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def get_with_retry(url, headers=None, params=None, max_retries=MAX_RETRIES):
    """Make a GET request with retries and exponential backoff.

    Args:
        url: URL to request
        headers: Optional headers dict
        params: Optional query parameters dict
        max_retries: Maximum number of retry attempts

    Returns:
        requests.Response object

    Raises:
        RuntimeError: If all retries fail
    """
    session = get_session()
    last_exception = None

    for attempt in range(max_retries):
        try:
            response = session.get(
                url,
                headers=headers,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            last_exception = e
            if attempt < max_retries - 1:
                wait_time = RETRY_BACKOFF_BASE ** attempt
                logger.warning(
                    f'Request failed (attempt {attempt + 1}/{max_retries}): {e}. '
                    f'Retrying in {wait_time}s...'
                )
                time.sleep(wait_time)
            else:
                logger.error(f'Request failed after {max_retries} attempts: {e}')

    raise RuntimeError(f'Failed to fetch {url} after {max_retries} retries: {last_exception}')


def get(url, max_retries=MAX_RETRIES):
    """Simple GET request with retry logic.

    Deprecated: Use get_with_retry() for more control.
    """
    return get_with_retry(url, max_retries=max_retries)

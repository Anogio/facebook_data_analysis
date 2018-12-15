import os
import pickle
from datetime import datetime

from dateutil import tz

from Python.global_vars import no_cache

_PROJECT_ROOT_DIR = os.path.join(os.path.dirname(__file__), '../../')
CACHE_FOLDER = 'cache'
OUTPUT_FOLDER = 'Output'


def resolve_path(*paths):
    return os.path.join(_PROJECT_ROOT_DIR, *paths)


output_path = resolve_path(OUTPUT_FOLDER)
if not os.path.isdir(output_path):
    os.makedirs(output_path)


def generate_sublists(list_to_split, max_sublist_size):
    """"
    Takes a list and returns a list of lists with a given maximum size
    """
    if not list_to_split:
        yield []

    else:
        breaks = list(range(0, len(list_to_split), max_sublist_size)) + [len(list_to_split)]

        start = breaks[0]
        for end in breaks[1:]:
            yield list_to_split[start:end]
            start = end


def timestamp_to_local_date(timestamp_ms):
    from_zone = tz.gettz('UTC')
    to_zone = tz.tzlocal()

    utc = datetime.utcfromtimestamp(timestamp_ms / 1000)
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)

    return local


def cached(file_name):
    def decorator(wrapped):
        cache_path = resolve_path(CACHE_FOLDER)
        file_path = resolve_path(CACHE_FOLDER, file_name)

        if not os.path.isdir(cache_path):
            os.makedirs(cache_path)

        def decorated(*args, **kwargs):
            if not os.path.isfile(file_path) or no_cache:
                res = wrapped(*args, **kwargs)
                with open(file_path, 'wb') as file:
                    pickle.dump(res, file)
            else:
                with open(file_path, 'rb') as file:
                    res = pickle.load(file)
            return res

        return decorated

    return decorator

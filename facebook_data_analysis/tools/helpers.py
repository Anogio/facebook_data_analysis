import hashlib
import os
import pickle
from datetime import datetime

from dateutil import tz
from facebook_data_analysis.global_vars import CACHE_FOLDER
from facebook_data_analysis.global_vars import OUTPUT_FOLDER

_PROJECT_ROOT_DIR = os.path.join(os.path.dirname(__file__), "../../")


def resolve_path(*paths):
    return os.path.join(_PROJECT_ROOT_DIR, *paths)


output_path = resolve_path(OUTPUT_FOLDER)
cache_path = resolve_path(CACHE_FOLDER)


def generate_sublists(list_to_split, max_sublist_size):
    """"
    Takes a list and returns a list of lists with a given maximum size
    """
    # TODO: replace with funcy.chunks
    if not list_to_split:
        yield []

    else:
        breaks = list(range(0, len(list_to_split), max_sublist_size)) + [
            len(list_to_split)
        ]

        start = breaks[0]
        for end in breaks[1:]:
            yield list_to_split[start:end]
            start = end


def timestamp_to_local_date(timestamp_ms):
    from_zone = tz.gettz("UTC")
    to_zone = tz.tzlocal()

    utc = datetime.utcfromtimestamp(timestamp_ms / 1000)
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)

    return local


def hash_string(string: str) -> str:
    return hashlib.md5(string.encode()).hexdigest()


def cached(file_name):
    def decorator(wrapped):
        def decorated(*args, **kwargs):
            file_name_with_args = (
                file_name + hash_string(str(*args) + str(**kwargs)) + ".cache"
            )
            file_path = resolve_path(CACHE_FOLDER, file_name_with_args)

            if not os.path.isdir(cache_path):
                os.makedirs(cache_path)

            if not os.path.isfile(file_path):
                res = wrapped(*args, **kwargs)
                with open(file_path, "wb") as file:
                    pickle.dump(res, file)
            else:
                with open(file_path, "rb") as file:
                    res = pickle.load(file)
            return res

        return decorated

    return decorator

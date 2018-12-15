import os

_PROJECT_ROOT_DIR = os.path.join(os.path.dirname(__file__), '../../')


def resolve_path(*paths):
    return os.path.join(_PROJECT_ROOT_DIR, *paths)


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

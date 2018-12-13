import os

_PROJECT_ROOT_DIR = os.path.join(os.path.dirname(__file__), '../../')


def resolve_path(*paths):
    return os.path.join(_PROJECT_ROOT_DIR, *paths)

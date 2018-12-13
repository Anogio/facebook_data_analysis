import requests
from tqdm import tqdm

from Python.tools.helpers import generate_sublists

API_URL = 'http://ip-api.com/batch'
DEFAULT_FIELDS = frozenset(['lat', 'lon', 'countryCode'])

MAX_API_BATCH_SIZE = 100


def format_one_ip(ip, required_fields=DEFAULT_FIELDS):
    return {'query': ip, 'fields': ','.join(required_fields)}


def get_ips_info_using_api(ips, required_fields=DEFAULT_FIELDS, max_batch=MAX_API_BATCH_SIZE):
    data = [format_one_ip(ip, required_fields) for ip in ips]

    all_responses = []

    with tqdm(total=len(ips)) as pbar:
        for sublist in tqdm(generate_sublists(data, max_batch)):
            all_responses += requests.post(API_URL, json=sublist).json()
            pbar.update()
    return all_responses

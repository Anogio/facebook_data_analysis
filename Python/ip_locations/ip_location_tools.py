import requests
from tqdm import tqdm

from Python.tools.data_getter import get_ips_list
from Python.tools.helpers import generate_sublists

API_URL = 'http://ip-api.com/batch'
DEFAULT_FIELDS = frozenset(['lat', 'lon', 'countryCode'])

MAX_API_BATCH_SIZE = 50


def format_one_ip(ip, required_fields=DEFAULT_FIELDS):
    return {'query': ip, 'fields': ','.join(required_fields)}


def get_ips_info_using_api(ips, required_fields=DEFAULT_FIELDS, max_batch=MAX_API_BATCH_SIZE):
    print('Getting location info for {} IP addresses'.format(len(ips)))
    data = [format_one_ip(ip, required_fields) for ip in ips]

    all_responses = []

    with tqdm(total=len(ips)) as pbar:
        for sublist in tqdm(generate_sublists(data, max_batch)):
            all_responses += requests.post(API_URL, json=sublist).json()
            pbar.update(len(sublist))
    return all_responses


def get_all_coordinates():
    ips = get_ips_list()
    coordinates = get_ips_info_using_api(ips, ['lon', 'lat'])

    return coordinates

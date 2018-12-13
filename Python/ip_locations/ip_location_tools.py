import requests

API_URL = 'http://ip-api.com/batch'
DEFAULT_FIELDS = frozenset(['lat', 'lon', 'countryCode'])


def format_one_ip(ip, required_fields=DEFAULT_FIELDS):
    return {'query': ip, 'fields': ','.join(required_fields)}


def get_ips(ips, required_fields=DEFAULT_FIELDS):
    data = [format_one_ip(ip, required_fields) for ip in ips]

    return requests.post(API_URL, json=data).json()

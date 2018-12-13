import json

from Python.tools.helpers import resolve_path

DATA_FOLDER = 'Data/'

IP_FILE = 'security_and_login_information/used_ip_addresses.json'


def get_file(file):
    with open(resolve_path(DATA_FOLDER + file), 'r') as file:
        return json.load(file)


def get_ips_list():
    ips = get_file(IP_FILE)

    return [entry['ip'] for entry in ips['used_ip_address']]

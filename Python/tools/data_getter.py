import json
import os

from Python.tools.helpers import resolve_path

DATA_FOLDER = 'Data'
CONVERSATIONS_FOLDER = 'messages'

IP_FILE = 'security_and_login_information/used_ip_addresses.json'


def get_file(file):
    with open(resolve_path(DATA_FOLDER, file), 'r') as file:
        return json.load(file)


def get_ips_list():
    ips = get_file(IP_FILE)
    return [entry['ip'] for entry in ips['used_ip_address']]


def get_conversations():
    conversations = []
    print('Retrieving conversations...')
    for path, subdirs, files in os.walk(resolve_path(DATA_FOLDER, CONVERSATIONS_FOLDER)):
        for name in files:
            if name == 'message.json':
                with open(os.path.join(path, name), 'r' ) as file:
                    conversations.append(json.load(file))
    total_mesages = sum([len(conversation['messages']) for conversation in conversations])
    print('Retrieved {} conversations with a total of {} messages'.format(len(conversations), total_mesages))
    return conversations

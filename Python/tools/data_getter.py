import json
import os
import re

from Python.tools.helpers import resolve_path

DATA_FOLDER = r'D:\Documents\FacebookData'
CONVERSATIONS_FOLDER = 'messages'

IP_FILE = 'security_and_login_information/used_ip_addresses.json'


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_file_from_data(file):
    return read_json(resolve_path(DATA_FOLDER, file))


def get_ips_list():
    ips = get_file_from_data(IP_FILE)
    return [entry['ip'] for entry in ips['used_ip_address']]


def get_conversations():
    conversations = []
    print('Retrieving conversations...')
    valid_file_name = re.compile('message_\d*.json')
    for path, subdirs, files in os.walk(resolve_path(DATA_FOLDER, CONVERSATIONS_FOLDER)):
        for name in files:
            if valid_file_name.match(name):
                conversations.append(read_json(os.path.join(path, name)))
    total_messages = sum([len(conversation['messages']) for conversation in conversations])
    print('Retrieved {} conversation json files with a total of {} messages'.format(len(conversations), total_messages))
    print()
    return conversations

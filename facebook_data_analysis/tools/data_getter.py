import json
import os
import re

from facebook_data_analysis.tools.helpers import resolve_path

CONVERSATIONS_FOLDER = "messages"

IP_FILE = "security_and_login_information/used_ip_addresses.json"


def read_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def get_file_from_data(file, data_folder):
    return read_json(os.path.join(data_folder, file))


def get_ips_list(data_folder):
    ips = get_file_from_data(IP_FILE, data_folder)
    return [entry["ip"] for entry in ips["used_ip_address"]]


def get_conversations(data_folder):
    conversations = []
    print("Retrieving conversations...")
    valid_file_name = re.compile(r"message_\d*.json")
    for path, _, files in os.walk(resolve_path(data_folder, CONVERSATIONS_FOLDER)):
        for name in files:
            if valid_file_name.match(name):
                conversations.append(read_json(os.path.join(path, name)))
    total_messages = sum(
        [len(conversation["messages"]) for conversation in conversations]
    )
    print(
        "Retrieved {} conversation json files with a total of {} messages".format(
            len(conversations), total_messages
        )
    )
    print()
    return conversations

import pandas as pd
import requests
from facebook_data_analysis.tools.data_getter import get_ips_list
from facebook_data_analysis.tools.helpers import cached
from facebook_data_analysis.tools.helpers import generate_sublists
from tqdm import tqdm

API_URL = "http://ip-api.com/batch"

MAX_API_BATCH_SIZE = 50


def format_one_ip(ip, required_fields):
    return {"query": ip, "fields": ",".join(required_fields)}


def get_ips_info_using_api(ips, required_fields, max_batch=MAX_API_BATCH_SIZE):
    print("Getting location info for {} IP addresses...".format(len(ips)))
    data = [format_one_ip(ip, required_fields) for ip in ips]

    all_responses = []

    with tqdm(total=len(ips)) as pbar:
        for sublist in tqdm(generate_sublists(data, max_batch)):
            all_responses += requests.post(API_URL, json=sublist).json()
            pbar.update(len(sublist))
    print()
    return all_responses


@cached("ip_coordinates")
def get_all_coordinates(data_folder):
    ips = get_ips_list(data_folder)
    coordinates = get_ips_info_using_api(
        ips, ["lon", "lat", "query", "city", "country"]
    )

    return pd.DataFrame(coordinates)

from Python.ip_locations.ip_location_tools import get_ips_info_using_api
from Python.tools.data_getter import get_ips_list


def get_all_coordinates():
    ips = get_ips_list()
    print('Getting location info for {} IP addresses'.format(len(ips)))
    return get_ips_info_using_api(ips, ['lon', 'lat'])

from data_bese import *
from user_agents import parse


def get_location_info(ip, simple_geoip):
    
    geoip_data = simple_geoip.get_geoip_data(ip)
    country = geoip_data['location']['country']

    if country != 'ZZ':
        city = geoip_data['location']['city']
    else:
        country = 'unknown'
        city = 'unknown'
    
    #na potrzeby testowania
    #country = 'unknown'
    #city = 'unknown'

    location = city + "," + country
    location = location.replace(' ', '')
    return location

def get_device(ua):
    user_agent = parse(ua)
    device = str(user_agent)
    device = device.replace(' ', '')
    device = device.replace('/', ',')
    return device


def check_if_new_device(username, device, location):
    user_id = get_user_by_username(username)[0]
    devices = get_autorized_devices_by_userid(user_id)
    isNew = True

    for deviceindb in devices:
        if deviceindb[0] == location and deviceindb[1]== device:
            isNew = False
            break

    return isNew
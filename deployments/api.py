import requests

import settings

headers = {
    'User-Agent': 'Bootloader-Agent/0.1',
    'Authorization': 'Token '+settings.API_TOKEN,
    'Content-Type': 'application/json',
    'Accepts': 'application/json',
}

DEPLOYMENTS_URL = '%sapi/deployments/' % settings.BOOTLOADER_URL
INTERFACES_URL = '%sapi/interfaces/' % settings.BOOTLOADER_URL
PROFILES_URL = '%sapi/profiles/' % settings.BOOTLOADER_URL
USERS_URL = '%sapi/users/' % settings.BOOTLOADER_URL


def download_file(URL, target):
    r = requests.get(URL)
    fp = open(target, 'w')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            fp.write(chunk)
    fp.close()


def get_deployment(deployment_id):
    r = requests.get(
        '%s%s/' % (DEPLOYMENTS_URL, deployment_id),
        headers=headers)
    deployment_object = r.json()

    return deployment_object


def get_interfaces_by_server(server):
    r = requests.get(
        '%s?server=%s' % (INTERFACES_URL, server),
        headers=headers
    )
    interfaces_object = r.json()

    return interfaces_object


def get_profile(profile_id):
    r = requests.get(
        '%s%s/' % (PROFILES_URL, profile_id),
        headers=headers)
    profile_object = r.json()

    return profile_object

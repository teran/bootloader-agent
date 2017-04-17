import requests

import settings

headers = {
    'User-Agent': 'Bootloader-Agent/0.1',
    'Authorization': 'Token '+settings.API_TOKEN,
    'Content-Type': 'application/json',
    'Accepts': 'application/json',
}

API_URL = '%sapi/v1alpha1' % (settings.BOOTLOADER_URL)

DEPLOYMENTS_URL = '%s/deployments/' % (API_URL)
INTERFACES_URL = '%s/interfaces/' % (API_URL)
PROFILES_URL = '%s/profiles/' % (API_URL)
USERS_URL = '%s/users/' % (API_URL)


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

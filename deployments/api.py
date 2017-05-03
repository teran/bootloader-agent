import json
import requests

import settings

headers = {
    'User-Agent': 'Bootloader-Agent/0.1',
    'Authorization': 'Token '+settings.API_TOKEN,
    'Content-Type': 'application/json',
    'Accepts': 'application/json',
}

API_URL = '%sapi/v1alpha1' % (settings.BOOTLOADER_URL)

CREDENTIALS_URL = '%s/credentials/' % (API_URL,)
DEPLOYMENTS_URL = '%s/deployments/' % (API_URL,)
INTERFACES_URL = '%s/interfaces/' % (API_URL,)
PROFILES_URL = '%s/profiles/' % (API_URL,)
SERVERS_URL = '%s/servers/' % (API_URL,)
USERS_URL = '%s/users/' % (API_URL,)


def download_file(URL, target):
    r = requests.get(URL)
    fp = open(target, 'w')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            fp.write(chunk)
    fp.close()


def get_credential(deployment_id, name):
    deployment = get_deployment(deployment_id)
    server = get_server(deployment['server'])

    credentials = requests.get(
        '%s?object=server&object_id=%s&name=%s' % (
            CREDENTIALS_URL, server['id'], name,),
        headers=headers
    ).json()

    print(credentials)
    return credentials[0]


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
    profile = json.loads(profile_object.get('profile'))

    return profile


def get_server(fqdn):
    r = requests.get(
        '%s?fqdn=%s' % (SERVERS_URL, fqdn),
        headers=headers)

    server_object = r.json()[0]

    return server_object

import requests

from furl import furl

import settings


headers = {
    'User-Agent': 'Bootloader-Agent/0.1',
    'Authorization': 'Token '+settings.API_TOKEN,
    'Content-Type': 'application/json',
    'Accepts': 'application/json',
}


def _api_request(
        object_name,
        object_id=None,
        query={},
        method='get',
        data=None):
    name = object_name+'s'
    API_URL = furl(
        settings.BOOTLOADER_URL).add(
            path='api').add(path=settings.API_VERSION).url
    handlers = requests.get(API_URL, headers=headers).json()

    if name in handlers.keys():
        handler_url = handlers[name]
    else:
        raise ValueError("No such handler available in API")

    url = handler_url
    if object_id is not None and isinstance(object_id, int):
        url = furl(url).add(path='/%s/' % (object_id,)).url
    if len(query) > 0:
        url = furl(url).add(query).url

    obj = None
    if method == 'delete':
        obj = requests.delete(url, headers=headers)
    elif method == 'get':
        obj = requests.get(url, headers=headers)
    elif method == 'post':
        obj = requests.post(url, headers=headers, data=data)
    elif method == 'put':
        obj = requests.put(url, headers=headers, data=data)
    else:
        raise ValueError("Method %s is not supported in _api_request()" % (
            method,))

    if obj.status_code not in (200, 201, 204):
        raise ApiQueryError(
            'Attempt to query %s is done with %s status code' % (
                object_name, obj.status_code,))

    return obj.json()


def download_file(URL, target):
    r = requests.get(URL)
    fp = open(target, 'w')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            fp.write(chunk)
    fp.close()


def get_credential(deployment_id, name):
    deployment = get_deployment(deployment_id)
    server = get_server_by_fqdn(deployment['server'])

    obj = _api_request(
        object_name='credential',
        query={
            'object': 'server',
            'object_id': server['id'],
            'name': name,
        })

    return obj[0]


def get_deployment(deployment_id):
    obj = _api_request(object_name='deployment', object_id=deployment_id)

    return obj


def get_interfaces_by_server(server):
    obj = _api_request(object_name='interface', query={'server': server})

    return obj


def get_profile(profile_id):
    obj = _api_request(object_name='profile', object_id=profile_id)

    return obj['profile']


def get_server_by_fqdn(fqdn):
    obj = _api_request(object_name='server', query={'fqdn': fqdn})

    return obj[0]


def get_server(server_id):
    obj = _api_request(object_name='server', object_id=server_id)

    return obj


class ApiQueryError(Exception):
    pass

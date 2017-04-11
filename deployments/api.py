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

def download_file(URL, target):
    r = requests.get(URL)
    fp = open(target, 'w')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            fp.write(chunk)
    fp.close()

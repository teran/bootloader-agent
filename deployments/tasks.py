#!/usr/bin/env python

import os

from celery import Celery
import requests

import settings

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)

headers = {
    'User-Agent': 'Bootloader-Agent/0.1',
    'Authorization': 'Token '+settings.API_TOKEN,
    'Content-Type': 'application/json',
    'Accepts': 'application/json',
}

DEPLOYMENTS_URL = '%sapi/deployments/' % settings.BOOTLOADER_URL
PROFILES_URL = '%sapi/profiles/' % settings.BOOTLOADER_URL

@app.task
def deployment_start(deployment):
    r = requests.get(
    '%s%s' % (DEPLOYMENTS_URL, deployment),
        headers=headers)
    deployment_object = r.json()

    r = requests.get(
        '%s%s' % (PROFILES_URL, deployment_object.get('profile')),
        headers=headers)
    profile_object = r.json()

    fileBase = 'export/file/%s/%s/%s/%s' % (
        deployment,
        deployment_object.get('token'),
        profile_object.get('name'),
        profile_object.get('version'))

    print fileBase

    download_file.apply_async(args=[
        'http://bootloader:8000/%s/pxelinux' % fileBase,
        '/tmp/test'
    ])


@app.task
def download_file(URL, target):
    r = requests.get(URL)
    fp = open(target, 'w')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            fp.write(chunk)
    fp.close()

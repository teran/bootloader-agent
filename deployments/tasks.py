#!/usr/bin/env python

import os

from celery import Celery
import requests

import settings

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)


@app.task
def deployment_start(deployment, profile, version, token):
    fileBase = 'export/file/%s/%s/%s/%s' % (
        deployment, token, profile, version)

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

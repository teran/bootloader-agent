#!/usr/bin/env python

import logging as logger
import os
import sys

from celery import Celery
import requests

import settings

if settings.API_TOKEN is None:
    logger.critical("No API token specified. Please refer to documentation")
    sys.exit(1)

import api

app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)

logger.basicConfig(format=settings.LOG_FORMAT)


@app.task
def deployment_start(deployment):
    r = requests.get(
        '%s%s/' % (api.DEPLOYMENTS_URL, deployment), headers=api.headers)
    deployment_object = r.json()

    r = requests.get(
        '%s%s/' % (api.PROFILES_URL, deployment_object.get('profile')),
        headers=api.headers)
    profile_object = r.json()

    fileBase = '%sexport/file/%s/%s/%s/%s' % (
        settings.BOOTLOADER_URL,
        deployment,
        deployment_object.get('token'),
        profile_object.get('name'),
        profile_object.get('version'))

    r = requests.get(
        '%s?server=%s' % (api.INTERFACES_URL, deployment_object.get('server')),
        headers=api.headers
    )
    interfaces_object = r.json()
    for interface in interfaces_object:
        download_file.apply_async(
            args=[
                '%s/%s' % (fileBase, 'pxelinux.cfg'),
                '/var/lib/tftp/pxelinux.cfg/01-%s' % interface.get(
                    'mac').replace(':', '-')])


@app.task
def download_file(URL, target):
    api.download_file(URL, target)


@app.task
def delete_file(target):
    os.unlink(target)

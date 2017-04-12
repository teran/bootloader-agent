#!/usr/bin/env python

import logging as logger
import os

from celery import Celery

import api
import settings


app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)

logger.basicConfig(format=settings.LOG_FORMAT)


@app.task
def deployment_start(deployment):
    deployment_object = api.get_deployment(
        deployment_id=deployment)
    profile_object = api.get_profile(
        profile_id=deployment_object.get('profile'))

    fileBase = '%sexport/file/%s/%s/%s/%s' % (
        settings.BOOTLOADER_URL,
        deployment,
        deployment_object.get('token'),
        profile_object.get('name'),
        profile_object.get('version'))

    interfaces_object = api.get_interfaces_by_server(
        deployment_object.get('server'))
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

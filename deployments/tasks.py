#!/usr/bin/env python

import logging as logger

from celery import Celery

import settings


app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)

logger.basicConfig(format=settings.LOG_FORMAT)


@app.task
def deployment_created(*args, **kwargs):
    print args, kwargs


@app.task
def evaluate_new(*args, **kwargs):
    print args, kwargs


@app.task
def evaluate_preparing(*args, **kwargs):
    print args, kwargs


@app.task
def evaluate_installing(*args, **kwargs):
    print args, kwargs


@app.task
def evaluate_configuring(*args, **kwargs):
    print args, kwargs


@app.task
def evaluate_postconfiguring(*args, **kwargs):
    print args, kwargs


@app.task
def evaluate_error(*args, **kwargs):
    print args, kwargs

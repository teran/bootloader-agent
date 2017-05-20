import os

from kombu import Queue

AGENT_URL = os.environ.get('AGENT_URL')

API_TOKEN = os.environ.get('API_TOKEN')

BOOTLOADER_URL = os.environ.get('BOOTLOADER_URL')

API_VERSION = 'v1alpha2'

USE_QUEUE = os.environ.get('QUEUE')

CALLBACK_DIR = '/var/lib/bootloader/callback'

CELERY_SETTINGS = {
    'BROKER_URL': os.environ.get(
        'BROKER_URL'),
    'CELERY_ACCEPT_CONTENT': ['json'],
    'CELERY_CREATE_MISSING_QUEUES': True,
    'CELERY_DEFAULT_QUEUE': USE_QUEUE,
    'CELERY_DEFAULT_EXCHANGE': None,
    'CELERY_DEFAULT_EXCHANGE_TYPE': 'direct',
    'CELERY_DEFAULT_ROUTING_KEY': 'task.default',
    'CELERY_IMPORTS': (
        'deployments.tasks',
        'deployments.tasks.AgentTasks',
    ),
    'CELERY_QUEUES': (
        Queue(USE_QUEUE, routing_key='deployment.#'),
    ),
    'CELERY_RESULT_BACKEND': 'rpc://',
    'CELERY_RESULT_SERIALIZER': 'json',
    'CELERY_ROUTES': {
            'tasks.deployment_start': {
                'queue': 'deployment',
                'routing_key': 'deployment_start',
            },
    },
    'CELERY_TASK_SERIALIZER': 'json',
}

LOG_FORMAT = os.environ.get(
    'LOG_FORMAT', '%(asctime)-15s %(levelname)s %(message)s')

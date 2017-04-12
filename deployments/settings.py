import os

from kombu import Queue

API_TOKEN = os.environ.get('API_TOKEN', None)

BOOTLOADER_URL = os.environ.get('BOOTLOADER_URL', 'http://bootloader:8000/')

USE_QUEUE = os.environ.get('QUEUE')

CELERY_SETTINGS = {
    'BROKER_URL': os.environ.get(
        'BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'),
    'CELERY_CREATE_MISSING_QUEUES': True,
    'CELERY_DEFAULT_QUEUE': USE_QUEUE,
    'CELERY_DEFAULT_EXCHANGE': 'tasks',
    'CELERY_DEFAULT_EXCHANGE_TYPE': 'topic',
    'CELERY_DEFAULT_ROUTING_KEY': 'task.default',
    'CELERY_QUEUES': (
        Queue(USE_QUEUE, routing_key='deployment.#'),
    ),
    'CELERY_ROUTES': {
            'tasks.deployment_start': {
                'queue': 'deployment',
                'routing_key': 'deployment_start',
            },
    }
}

LOG_FORMAT = os.environ.get(
    'LOG_FORMAT', '%(asctime)-15s %(levelname)s %(message)s')

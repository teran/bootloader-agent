import os

from kombu import Queue

API_TOKEN=os.environ.get('API_TOKEN', 'a27db5e91adeb69b44a51b61600127726573e519')

BOOTLOADER_URL = os.environ.get('BOOTLOADER_URL', 'http://bootloader:8000/')

CELERY_SETTINGS = {
    'BROKER_URL': os.environ.get('BROKER_URL', 'amqp://guest:guest@rabbitmq:5672//'),
    'CELERY_CREATE_MISSING_QUEUES': True,
    'CELERY_DEFAULT_QUEUE': 'default',
    'CELERY_DEFAULT_EXCHANGE': 'tasks',
    'CELERY_DEFAULT_EXCHANGE_TYPE': 'topic',
    'CELERY_DEFAULT_ROUTING_KEY': 'task.default',
    'CELERY_QUEUES': (
        Queue('default', routing_key='task.#'),
        Queue('deployment', routing_key='deployment.#'),
    ),
    'CELERY_ROUTES': {
            'tasks.deployment_start': {
                'queue': 'deployment',
                'routing_key': 'deployment_start',
            },
    }
}
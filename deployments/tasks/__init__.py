from celery import Celery

from deployments import settings


app = Celery('tasks')
app.conf.update(**settings.CELERY_SETTINGS)

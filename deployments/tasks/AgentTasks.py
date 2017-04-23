import os
import time

from deployments import api
from deployments import settings
from deployments.tasks import app


@app.task
def download_file(deployment, source, destination):
    print('download_file evaluating for %s: %s --> %s' % (
        deployment, source, destination))
    import requests

    r = requests.get(source)

    try:
        os.makedirs(os.path.dirname(destination))
    except OSError as e:
        if e.message == 'File exists':
            pass

    with open(destination, 'w') as fp:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
    return True


@app.task
def delete_file(deployment, filename):
    print('delete_file on %s is not implemented yet')

    return True


@app.task
def echo(message):
    print('Echo: %s' % (message))


@app.task(bind=True)
def expect_callback(self, deployment, callback_name):
    print('expect_callback evaluating for %s: %s' % (
        deployment, callback_name))
    import os

    d = api.get_deployment(deployment)

    path = os.path.join(
        str(settings.CALLBACK_DIR),
        str(d['token']),
        str(callback_name))

    print('expect_callback on %s' % path)

    while not os.path.exists(path):
        print('Callback %s is not ready yet, waiting 30 secs' % path)
        time.sleep(30)

    print('Callback found: %s' % path)


@app.task
def ipmi_command(deployment, command):
    print('ipmi_command evaluating for %s: %s' % (deployment, command))

    return True

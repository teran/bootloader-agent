import os
import requests
import time

from deployments import api, settings


class Workflow():
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def download_file(self, deployment, source, destination):
        print('download_file evaluating for %s: %s --> %s' % (
            deployment, source, destination))

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

    def delete_file(self, deployment, filename):
        print('delete_file on %s is not implemented yet')

    def echo(self, message):
        print('Echo: %s' % (message))

    def expect_callback(self, deployment, callback_name):
        print('expect_callback evaluating for %s: %s' % (
            deployment, callback_name))

        d = api.get_deployment(deployment)

        path = os.path.join(
            str(settings.CALLBACK_DIR),
            str(d['token']),
            str(callback_name))

        print('expect_callback on %s' % path)

        while not os.path.exists(path):
            print('Callback %s is not ready yet, waiting 3 secs' % path)
            time.sleep(3)

        print('Callback found: %s' % path)

    def ipmi_command(self, deployment, command):
        print('ipmi_command evaluating for %s: %s' % (deployment, command))

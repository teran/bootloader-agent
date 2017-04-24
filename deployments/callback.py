import os
from flask import Flask

from deployments import settings


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/_callback/<string:token>/<string:name>')
def callback(token, name):
    path = os.path.join(
        str(settings.CALLBACK_DIR),
        str(token),
        str(name))

    try:
        os.makedirs(os.path.dirname(path))
    except OSError as e:
        if e.message == 'File exists':
            pass

    if not os.path.exists(path):
        open(path, 'w').close()

    return 'Ok', 201

from deployments.tasks import app
from deployments.workflow import Workflow


@app.task
def evaluate(deloyment, pipeline):
    """
    pipeline = [
        {
            'action': 'download_file'
            'deployment': 11111,
            'source': 'http://....../kernel'
            'destination': '/var/lib/tftp/blah'
        }
    ]
    """

    w = Workflow(pipeline=pipeline)

    for step in pipeline:
        if type(step) == type({}):
            action = step['action']
            del(step['action'])

            getattr(w, action)(**step)
        elif type(step) in (type([]), type(()),):
            for substep in step:
                action = substep['action']
                del(substep['action'])

                getattr(w, action)(**substep)

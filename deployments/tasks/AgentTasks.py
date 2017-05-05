from deployments import api, settings
from deployments.tasks import app
import requests
import os
import time


@app.task
def download_file(deployment, source, destination):
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


@app.task
def delete_file(deployment, filename):
    print('delete_file on %s is not implemented yet')


@app.task
def echo(message):
    print('Echo: %s' % (message))


@app.task
def expect_callback(deployment, callback_name):
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


@app.task
def ipmi_command(deployment, command, parameters=None):
    print('ipmi_command evaluating for %s: %s' % (deployment, command))

    from pyghmi.ipmi import command

    d = api.get_deployment(deployment)
    s = api.get_server_by_fqdn(d['server'])

    ipmi_username = api.get_credential(d['id'], 'ipmi_username')['data']
    ipmi_password = api.get_credential(d['id'], 'ipmi_password')['data']

    def docommand(result, ipmisession):
        print("IPMI sesssion established to %s" % (ipmisession.bmc,))

        if 'error' in result:
            print('Error occured: %s' % (result,))
            print(None)

        if command == 'bootdev':
            if parameters:
                print(ipmisession.set_bootdev(parameters))
            else:
                print(ipmisession.get_bootdev())
        elif command == 'health':
            print(ipmisession.get_health())
        elif command == 'inventory':
            print(ipmisession.get_inventory())
        elif command == 'leds':
            print(ipmisession.get_leds())
        elif command == 'net':
            print(ipmisession.get_net_configuration())
        elif command == 'power':
            if parameters:
                print(ipmisession.set_power(parameters, wait=True))
            else:
                print(ipmisession.get_power()['powerstate'])
        elif command == 'sensors':
            print(ipmisession.get_sensor_data())

    ipmicmd = command.Command(
        bmc=s['ipmi_host'],
        userid=ipmi_username,
        password=ipmi_password,
        onlogon=docommand)
    ipmicmd.eventloop()

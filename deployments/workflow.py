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

    def ipmi_command(self, deployment, command, action=None):
        print('ipmi_command evaluating for %s: %s' % (deployment, command))

        from pyghmi.ipmi import command

        d = api.get_deployment(deployment)
        s = api.get_server(d['server'])

        def docommand(result, ipmisession):
            print("IPMI sesssion established to %s" % (ipmisession.bmc,))

            if 'error' in result:
                print('Error occured: %s' % (result,))
                return None

            if command == 'bootdev':
                if action:
                    return ipmisession.set_bootdev(action)
                else:
                    return ipmisession.get_bootdev()
            elif command == 'health':
                return ipmisession.get_health()
            elif command == 'inventory':
                return ipmisession.get_inventory()
            elif command == 'leds':
                return ipmisession.get_leds()
            elif command == 'net':
                return ipmisession.get_net_configuration()
            elif command == 'power':
                if action:
                    return ipmisession.set_power(action, wait=True)
                else:
                    return ipmisession.get_power()['powerstate']
            elif command == 'sensors':
                return ipmisession.get_sensor_data()

        ipmicmd = command.Command(
            bmc=s['ipmi_host'],
            userid=s['ipmi_username'],
            password=s['ipmi_password'],
            onlogon=docommand)
        ipmicmd.eventloop()

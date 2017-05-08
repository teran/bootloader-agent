#!/bin/sh

set -e

[[ -z "${AGENT_URL}" ]] && \
  echo "No agent URL specified" && exit 1
[[ -z "${QUEUE}" ]] && \
  echo "No queue specified" && exit 1
[[ -z "${API_TOKEN}" ]] && \
  echo "No API token specified" && exit 1

RUN_TFTP=${RUN_TFTP:=false}
RUN_DHCP=${RUN_DHCP:=false}
RUN_HTTP=${RUN_HTTP:=false}

DHCP_BOOT_FILENAME=${DHCP_BOOT_FILENAME:=lpxelinux.0}

DNSMASQ_CMD="/usr/sbin/dnsmasq"

if [[ "${RUN_TFTP}" == "true" ]] ; then
  DNSMASQ_CMD="${DNSMASQ_CMD} --enable-tftp --tftp-root=/var/lib/tftp"
fi

if [[ "${RUN_DHCP}" == "true" ]] ; then
  [[ -z "${DHCP_RANGE}" ]] && \
    echo "No DHCP_RANGE specified" && exit 1
  [[ -z "${DHCP_NETMASK}" ]] && \
    echo "No DHCP_NETMASK specified" && exit 1
  [[ -z "${DHCP_ROUTER}" ]] && \
    echo "No DHCP_ROUTER specified" && exit 1

  DNSMASQ_CMD="${DNSMASQ_CMD} --dhcp-range=${DHCP_RANGE} --dhcp-option=option:netmask,${DHCP_NETMASK}"
  DNSMASQ_CMD="${DNSMASQ_CMD} --dhcp-option=option:router,${DHCP_ROUTER} --dhcp-boot=${DHCP_BOOT_FILENAME}"
fi

DNSMASQ_CMD="${DNSMASQ_CMD} ${DNSMASQ_OPTS}"

if [[ "${RUN_TFTP}" == "true" ]] || [[ "${RUN_DHCP}" == "true" ]] ; then
  $DNSMASQ_CMD
fi

touch /var/log/uwsgi.log
mkdir -p /run/uwsgi /var/lib/bootloader/callback
chown nobody:nogroup /var/log/uwsgi.log /run/uwsgi /var/lib/bootloader/callback
chmod 0600 /var/log/uwsgi.log

uwsgi \
  -y /etc/bootloader/uwsgi.yaml \
  --daemonize2 /var/log/uwsgi.log \
  --pidfile2 /run/uwsgi/uwsgi.pid

if [[ "${RUN_HTTP}" == "true" ]] ; then
  mkdir -p /run/nginx
  nginx -t && nginx
else
  echo
  echo ">>>> WARNING! HTTP server is not enabled!!!"
  echo ">>>> HTTP server is required to use serve_file(via http) and expect_callback statemens"
  echo
fi

touch /var/log/celery.log
chown bootloader:nobody /var/log/celery.log
chmod 0600 /var/log/celery.log
mkdir -p /run/celery
chown bootloader:nobody /run/celery

/usr/bin/celery worker \
  --app deployments.tasks \
  --queues ${QUEUE} \
  --logfile /var/log/celery.log \
  --pidfile=/run/celery/celery.pid \
  --uid 100 \
  --gid 65533 \
  --detach


trap 'echo "Killing processes..." ; \
      kill $(cat /run/celery/celery.pid) ; \
      kill -SIGINT $(cat /run/uwsgi/uwsgi.pid) ; \
      kill $(cat /run/nginx/nginx.pid) ; \
      sleep 2' \
  SIGINT SIGTERM

tail -f /var/log/uwsgi.log /var/log/nginx/* /var/log/celery.log

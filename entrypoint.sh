#!/bin/sh

set -e

[[ -z "${QUEUE}" ]] && \
  echo "No queue specified" && exit 1
[[ -z "${API_TOKEN}" ]] && \
  echo "No API token specified" && exit 1

RUN_TFTP=${RUN_TFTP:=false}
DHCP_BOOT_FILENAME=${DHCP_BOOT_FILENAME:=lpxelinux.0}

DNSMASQ_CMD="/usr/sbin/dnsmasq"

if [[ "${RUN_TFTP}" == "true" ]] ; then
  DNSMASQ_CMD="${DNSMASQ_CMD} --enable-tftp --tftp-root=/var/lib/tftp"
fi

if [[ -n "${RUN_DHCP}" ]] ; then
  DNSMASQ_CMD="${DNSMASQ_CMD} --dhcp-range=${RUN_DHCP} --dhcp-boot=${DHCP_BOOT_FILENAME}"
  DNSMASQ_CMD="${DNSMASQ_CMD} --dhcp-option=vendor:PXEClient,6,2b --dhcp-no-override"
fi

DNSMASQ_CMD="${DNSMASQ_CMD} ${DNSMASQ_OPTS}"

if [[ "${RUN_TFTP}" == "true" ]] || [[ -n "${RUN_DHCP}" ]] ; then
  $DNSMASQ_CMD
fi

/bin/su -c "/usr/bin/celery -A deployments.tasks worker -Q ${QUEUE}" bootloader

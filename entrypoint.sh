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

if [[ "${RUN_TFTP}" == "true" ]] || [[ -n "${RUN_DHCP}" ]] ; then
  $DNSMASQ_CMD
fi

/bin/su -c "/usr/bin/celery -A deployments.tasks worker -Q ${QUEUE}" bootloader

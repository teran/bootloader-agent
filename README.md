# Bootloader-Agent

[![Build Status](https://travis-ci.org/teran/bootloader-agent.svg?branch=master)](https://travis-ci.org/teran/bootloader-agent)
[![Layers size](https://images.microbadger.com/badges/image/teran/bootloader-agent.svg)](https://hub.docker.com/r/teran/bootloader-agent/)
![Recent build commit](https://images.microbadger.com/badges/commit/teran/bootloader-agent.svg)
[![Docker Automated build](https://img.shields.io/docker/automated/teran/bootloader-agent.svg)](https://hub.docker.com/r/teran/bootloader-agent/)
![License](https://img.shields.io/github/license/teran/bootloader-agent.svg)

Agent application for [bootloader-web](https://github.com/teran/bootloader-web)
to serve as proxy for requests require L2 connectivity such as DHCP and in some
cases TFTP for faster downloads.

Currently deep-deep alpha state.

Configuration
=============

Currently there's the way to configure the agent via environment variables:

 * `API_TOKEN` - bootloader-web API access token, default is `None`
 * `BOOTLOADER_URL` - URL of bootloader-web instance, default is `'http://bootloader:8000/'`
 * `BROKER_URL` - URL of broker for celery, default is `'amqp://guest:guest@rabbitmq:5672//'`
 * `DHCP_BOOT_FILENAME` - filename to use for PXE boot. Builtin files are: `pxelinux.0`, `lpxelinux.0` - default
 * `DHCP_NETMASK` - netmask in IP form to serve by DHCP, example: `255.255.255.0`
 * `DHCP_RANGE` - `<range_start>,<range_end>,<lease_duration>` formated string
 * `DHCP_ROUTER` - network router to serve by DHCP, example: `10.0.30.254`
 * `DNSMASQ_OPTS` - custom options to be passed to dnsmasq.
    Example:
    ```
    DNSMASQ_OPTS="--dhcp-option=option:ntp-server,192.168.0.5"
    ```
 * `LOG_FORMAT` - log record format string. [As Python template](https://docs.python.org/dev/library/logging.html#logrecord-attributes)
 * `QUEUE` - queue name generated by [bootloader-web](https://github.com/teran/bootloader-web) for particular location
 * `RUN_DHCP` - `true|false` should we enable DHCP server or not
 * `RUN_HTTP` - `true|false` should we enable HTTP server or not
 * `RUN_TFTP` - `true|false` should we enable TFTP server or not

Run example
===========

```
docker run -it --cap-add NET_ADMIN --network=host \
  -e API_TOKEN=<bootloader_api_token> \
  -e BOOTLOADER_URL=http://bootloader.example.org/ \
  -e DHCP_NETMASK=255.255.255.0 \
  -e DHCP_RANGE=192.168.0.100,192.168.0.200,3h \
  -e DHCP_ROUTER=192.168.0.254 \
  -e DNSMASQ_OPTS='--dhcp-option=option:ntp-server,192.168.0.254' \
  -e QUEUE=deployment-1-mylocationname \
  -e RUN_DHCP=true \
  -e RUN_HTTP=true \
  -e RUN_TFTP=true \
    teran/bootloader-agent
```

Licence
=======

The code is licenced under GPLv2 licence.

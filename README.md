# Bootloader-Agent

[![Docker Automated build](https://img.shields.io/docker/automated/teran/bootloader-agent.svg)](https://hub.docker.com/r/teran/bootloader-agent/)
[![License](https://img.shields.io/github/license/teran/bootloader-agent.svg)]()

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

Licence
=======

The code is licenced under GPLv2 licence.

FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      freetype-dev \
      g++ \
      gcc \
      git \
      linux-headers \
      pkgconfig \
      python \
      python-dev \
      py2-pip \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN adduser -SDHh /opt/bootloader/agent -s /bin/sh bootloader

WORKDIR "/opt/bootloader/agent"

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ADD requirements.txt /opt/bootloader/agent/

RUN pip install --no-cache-dir --upgrade -r /opt/bootloader/agent/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

USER bootloader

ADD deployments /opt/bootloader/agent/deployments

ENTRYPOINT ["celery", "-A", "deployments.tasks", "worker"]

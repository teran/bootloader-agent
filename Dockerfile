FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      dnsmasq \
      freetype-dev \
      g++ \
      gcc \
      git \
      linux-headers \
      pkgconfig \
      python \
      python-dev \
      py2-pip \
      syslinux \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN adduser -SDHh /opt/bootloader/agent -s /bin/sh bootloader
RUN mkdir -p /var/lib/tftp/pxelinux.cfg && \
    chown -R bootloader:nogroup /var/lib/tftp

RUN cp /usr/share/syslinux/pxelinux.0 /var/lib/tftp/pxelinux.0 && \
    cp /usr/share/syslinux/lpxelinux.0 /var/lib/tftp/lpxelinux.0

WORKDIR "/opt/bootloader/agent"

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ADD requirements.txt /opt/bootloader/agent/

RUN pip install --no-cache-dir --upgrade -r /opt/bootloader/agent/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

USER bootloader

ADD deployments /opt/bootloader/agent/deployments

ENTRYPOINT ["celery", "-A", "deployments.tasks", "worker"]

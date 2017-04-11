FROM alpine:latest

EXPOSE 67/udp
EXPOSE 69/udp
EXPOSE 80

RUN apk --update --no-cache add \
      ca-certificates \
      dnsmasq \
      nginx \
      python \
      py2-pip \
      syslinux \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

ADD nginx.conf /etc/nginx/nginx.conf

RUN adduser -SDHh /opt/bootloader/agent -s /bin/sh bootloader
RUN mkdir -p /var/lib/tftp/pxelinux.cfg && \
    chown -R bootloader:nogroup /var/lib/tftp

RUN cp /usr/share/syslinux/pxelinux.0 /var/lib/tftp/pxelinux.0 && \
    cp /usr/share/syslinux/lpxelinux.0 /var/lib/tftp/lpxelinux.0

WORKDIR "/opt/bootloader/agent"

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ADD requirements.txt /opt/bootloader/agent/

RUN apk add --update --no-cache \
      freetype-dev \
      g++ \
      gcc \
      git \
      linux-headers \
      pkgconfig \
      python-dev && \
    pip install --no-cache-dir --upgrade -r /opt/bootloader/agent/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete && \
    apk del --update --purge --no-cache \
      freetype-dev \
      g++ \
      gcc \
      git \
      linux-headers \
      pkgconfig \
      python-dev

ADD deployments /opt/bootloader/agent/deployments
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

FROM python:3.7

RUN apt-get update -yqq \
    && apt-get install -yqq \
    collectd \
    supervisor

RUN mkdir -p /opt/collectd_plugins

COPY ./collectd.conf /etc/collectd/collectd.conf

FROM ubuntu:18.04
MAINTAINER Aric Parkinson <aric.parkinson@gmail.com>

RUN apt-get update && \
    apt-get install -y \
        libpq-dev \
        python3 \
        python3-pip

COPY dip_server/ /opt/verbose_carnival/dip_server/
WORKDIR /opt/verbose_carnival/dip_server/
RUN pip3 install -r requirements.txt

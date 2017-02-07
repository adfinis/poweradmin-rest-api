FROM debian:stable
MAINTAINER Patrick Winter <patrick.winter@adfinis-sygroup.ch>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qqy && apt-get upgrade -qqy
RUN apt-get install -qqy pdns-server pdns-backend-mysql

WORKDIR /etc/powerdns
RUN rm bindbackend.conf /etc/powerdns/pdns.d/*
ADD mysql.conf /etc/powerdns/pdns.d/mysql.conf

CMD pdns_server --daemon=no --guardian=no --control-console --loglevel=9

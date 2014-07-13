# basic stack Dockerfile starting from minicf/minicf
# 
# this is used to build the docker image for an application
FROM ubuntu:14.04
MAINTAINER ps@novapp.ch
ADD ./bin /bin 
RUN /bin/detect /app
RUN /bin/compile /app
RUN /bin/release /app

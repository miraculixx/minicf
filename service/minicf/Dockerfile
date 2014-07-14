# basic stack Dockerfile starting from minicf/minicf
# 
# this is used to build the docker image for an application
FROM stack/minicf
MAINTAINER ps@novapp.ch
ADD ./bin /bin 
RUN /bin/detect /app
RUN /bin/compile /app
RUN /bin/release /app
CMD /bin/start
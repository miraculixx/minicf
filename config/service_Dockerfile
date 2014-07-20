# basic stack Dockerfile
# 
# this is used to build the docker image for an application
FROM stack/minicf
MAINTAINER ps@novapp.ch
ADD ./bin /bin
ADD ./app /app
ADD ./log /log 
CMD /bin/start
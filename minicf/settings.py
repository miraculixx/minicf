'''
Created on Jul 13, 2014

@author: patrick
'''
from minimongo.options import configure
import os
import sys

BIN_DIR='/usr/local/minicf/bin'
GIT_HOME='/opt/git'
DB_URL='localhost:27017'
DOCKER_URL='unix://var/run/docker.sock'
DEFAULT_MANIFEST = {
   'framework' : 'stack/minicf'
}

# configure minimongo ORM
# by doing this here we don't have to specify
# this in every single model class
# for more settings see minimongo.options._Options
MONGODB_HOST=DB_URL.split(':')[0]
MONGODB_PORT=int(DB_URL.split(':')[1])
MONGODB_DATABASE='minicf'

# change settings for test runs
# this can't be done at runtime so we do it here
if os.environ.get('MINICF_TEST'):
    MONGODB_DATABASE='testdb'
    GIT_HOME='/opt/git'
    


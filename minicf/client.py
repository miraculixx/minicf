'''
Created on Jul 13, 2014

@author: patrick
'''
from controller import MiniCFController
from fabric.api import env
from fabric.decorators import task
from fabric.operations import local

@task
def push(app=None):
    print "pushing %s" % app

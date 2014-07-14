"""
Controller fabfile
"""
from fabric.decorators import task
from fabric.operations import local
import os

@task
def start():
    """
    start the application 
    """
    if not os.path.isfile('/app/manifest.yml'):
        print "minicf basic setup"
        print "you have to provide a manifest.yml"
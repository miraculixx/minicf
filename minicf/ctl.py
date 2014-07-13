"""
Controller fabfile
"""
from fabric.decorators import task
from fabric.operations import local
from minicf.controller import MiniCFController

@task(alias='build-image')
def buildimage(buildpack=None):
    ctl = MiniCFController()
    ctl.build_image(buildpack)
    
@task
def cleanup():
    """
    remove containers and images for good
    """
    # remove containers
    local('docker ps -a | cut -d' ' -f1  | xargs docker rm')
    # remove images
    local('docker images | grep -v ubuntu | cut -c41-50 | tail -n+2 | docker rmi')
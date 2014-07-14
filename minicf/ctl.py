"""
Controller fabfile
"""
from controller import MiniCFController
from fabric.decorators import task
from fabric.operations import local
from fabric.context_managers import settings
    
@task
def cleanup():
    """
    remove containers and images for good
    """
    # remove containers
    with settings(warn_only=True):
        local("docker ps -a | tail -n+2 | cut -d' ' -f1  | xargs docker rm")
        # remove images, but leave ubuntu there
        local('docker images | grep -v ubuntu | cut -c41-50 | tail -n+2 | xargs docker rmi')

@task(alias='build-image')
def buildimage(buildpack=None):
    """
    build stack or service image
    """
    ctl = MiniCFController()
    ctl.create_buildpack_image(buildpack)

@task(alias='build-stack')
def buildstack(image=None, buildpacks=None):
    """
    build a stack from multiple buildpacks (bp1;bp2;bp3)
    """
    ctl = MiniCFController()
    buildpacks = buildpacks.split('+')
    ctl.create_combined_image(image, buildpacks)
    
@task(alias='build-app')
def buildapp(user=None, appname=None, manifest=None):
    """
    build app image
    """
    if not user:
        print "Specify user="
    if not appname:
        print "Specify appname="
    ctl = MiniCFController()
    ctl.create_app_image(user, appname, manifest)

@task(alias='create-app')
def createapp(user=None, appname=None):
    """
    add the git repository for the app
    """
    if not user:
        print "Specify user="
    if not appname:
        print "Specify appname="
    ctl = MiniCFController()
    ctl.create_git(user, appname)

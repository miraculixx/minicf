'''
Created on Jul 13, 2014

@author: patrick
'''
from fabric.context_managers import settings
from fabric.decorators import task, roles
from fabric.operations import local, run, put
from fabric.state import env

env.roledefs = {
  'minicf' : ['novapp.digoc.com']
}
env.use_ssh_config = True

INSTALL_DIR='/usr/local/minicf'

@task
def package():
    local('tar -czf dist/minicf.tgz --exclude dist --exclude env --exclude .git .')

def copyfiles():
    with settings(warn_only=True):
        run('rm -rf %s' % INSTALL_DIR)
        run('mkdir %s' % INSTALL_DIR)
        put('dist/minicf.tgz', '/tmp')
        run('tar -C %s -xzf /tmp/minicf.tgz' % INSTALL_DIR)
        
@task
@roles('minicf')
def uninstall():
    with settings(warn_only=True):
        run('%s/bin/uninstall' % INSTALL_DIR)
        run('rm -rf %s' % INSTALL_DIR)
    
@task
@roles('minicf')
def setup():
    """
    perform the basic setup and installation
    """
    copyfiles()
    run('chmod +x %s/bin/install' % INSTALL_DIR)
    run('%s/bin/install' % INSTALL_DIR)
    
@task
@roles('minicf')
def update():
    """
    upate minicf 
    """
    copyfiles()
    
@task
@roles('minicf')
def test():
    """
    run tests
    """
    run('%s/bin/test' % INSTALL_DIR)
    
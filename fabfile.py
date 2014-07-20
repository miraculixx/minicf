'''
Created on Jul 13, 2014

@author: patrick
'''
from fabric.context_managers import settings
from fabric.decorators import task, roles
from fabric.operations import local, run, put
from fabric.state import env
import digitalocean

env.roledefs = {
  'minicf' : ['novapp.digoc.com']
}
env.use_ssh_config = True

INSTALL_DIR='/usr/local/minicf'

@task
def package():
    local('tar -czf dist/minicf.tgz --exclude dist --exclude env --exclude .git .')

def copyfiles():
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
    with settings(warn_only=True):
        run('rm -rf %s' % INSTALL_DIR)
        run('mkdir %s' % INSTALL_DIR)
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
    run('%s/bin/update' % INSTALL_DIR)
    
@task
@roles('minicf')
def test(test="minicf.tests"):
    """
    run tests
    """
    run('%s/bin/test %s' % (INSTALL_DIR, test))
    
def list_droplets(droplets, *args):
    for droplet in droplets:
        print "-" * 10
        for k,v in droplet.__dict__.iteritems():
            print k,v

def start_droplet(droplets, name):
    if name:
        droplet = [d for d in droplets if d.name == name][0]
        droplet.power_on()
        print "OK, %s started." % name
    else:
        for droplet in droplets:
            droplet.power_on()
            print "OK, %s started" % droplet.name
    
def stop_droplet(droplets, name):
    if name:
        droplet = [d for d in droplets if d.name == name][0]
        droplet.power_off()
        print "OK, %s stopped." % name
    else:
        for droplet in droplets:
            droplet.power_off()
            print "OK, %s stopped." % droplet.name
    
    
def restart_droplet(droplets, name):
    if name:
        droplet = [d for d in droplets if d.name == name][0]
        droplet.power_cycle()
        print "OK, %s restarted." % name
    else:
        for droplet in droplets:
            droplet.power_cycle()
            print "OK, %s restarted." % droplet.name
    
    
@task
def droplet(command="list", *args):
    """
    droplet interaction, list/start/stop/restart,name
    """
    import yaml
    # read digitalocean api key
    with open('.digitalocean/client.yml') as f:
        """
        you need a ./digitalocean/client.yml with the following
        properties. Note these codes are for API v1!
        
        minicf:
            client_id: <your client id>
            api_key: <your api key>
        """
        cfg = yaml.safe_load(f)
    # configure digital ocean
    manager = digitalocean.Manager(**cfg['minicf'])
    # get droplets 
    droplets = manager.get_all_droplets()
    # parse and process command
    # -- each command is associated with a droplet
    #    function that takes the droplets list plus
    #    an optional list of arguments
    commands={
       'list' : list_droplets,     
       'start' : start_droplet,
       'stop' : stop_droplet,
       'restart' : restart_droplet  
    }
    args = args or [None]
    if command in commands:
        commands[command](droplets, *args)
        
"""
Controller fabfile
"""
from fabric.decorators import task
from fabric.operations import local
import os
import yaml

@task
def start():
    """
    start the application 
    """
    if not os.path.isfile('/app/manifest.yml'):
        print "minicf basic setup"
        print "you have to provide a manifest.yml"
    with open('/app/manifest.yml') as f:
        manifest = yaml.safe_load(f)
    manifest = manifest or {
      'docker-run' : {
        'command' : 'echo No command given'
      }
    }
    # get docker run commands
    for cmd in manifest.get('docker-run'):
        command = cmd.get('command')
    
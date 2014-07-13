'''
Created on Jul 13, 2014

@author: patrick
'''
import docker

class MiniCFDocker(object):
    """
    Use docker as minicf's IaaS provider. Any command that
    the controller issues to create a new VM is served
    by this. We use this to abstract the interface between
    the controller and docker (or any other IaaS provider) 
    """
    # public methods
    def create(self):
        c = self.connect()
        cid = c.create_container('ubuntu:14.04')
        
    # internal methods    
    def connect(self):
        """
        connect to the docker client
        see https://github.com/dotcloud/docker-py
        """
        c = docker.Client(base_url='unix://var/run/docker.sock',
                  version='1.12',
                  timeout=10)
        return c
    
    
        
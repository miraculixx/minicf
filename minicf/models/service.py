'''
Created on Jul 19, 2014

@author: patrick
'''
from minimongo.model import Model
from minimongo.options import configure
from minicf import settings

class Service(Model):
    """
    A simple model for services
    
    app = Service({
                'user' : user,
                'name' : appname,
                'manifest' : manifest
            })
    """
    class Meta:
        collection = 'services'
        
    
        
    

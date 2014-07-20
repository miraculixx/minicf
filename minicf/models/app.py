'''
Created on Jul 19, 2014

@author: patrick
'''
from minimongo.model import Model
from minimongo.options import configure
from minicf import settings

class App(Model):
    """
    A simple model for apps
    
    app = App({
                'user' : user,
                'name' : appname,
                'git' : gituri,
                'docker' : dockerid,
                'manifest' : manifest
            })
    """
    class Meta:
        collection = 'apps'
        
    
        
    

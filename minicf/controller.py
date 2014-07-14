'''
Created on Jul 13, 2014

@author: patrick
'''
from fabric.operations import local
from minicf.shutil import sh, mkdir, cd, git
from pymongo.mongo_client import MongoClient
import os
import settings

# commands
hostname = sh('hostname')
tar = sh('tar')
cp = sh('cp')


class MiniCFController(object):
    """
    A single machine mini cloudfoundry controller that uses
    docker to run containers. It mimicks the following commands of
    cloudfoundry 
    
    login
    push <appname>
    start <appname>
    stop <appname>
    restart <appname>
    delete <appname>
    update <appname>
    create-service <service>
    bind-service <service> <appname>
    unbind-service <service> <appname>
    delete-service <service>
    """
    
    # public methods
    def login(self, user, password):
        """
        login the user onto the service
        """
        self.user = 'demo'
        return True 
    
    def create_app(self, user, appname, manifest):
        """
        create a new app. this is called by the push command
        and will do the following:
        
        1. setup a new git repository for this app
        2. create a new docker container
        3. register the repository and the app
        
        @param appname the name of the app
        @manifest manifest the parsed manifest YML   
        """
        try:
            gituri = self.create_git(user, appname)
            dockerid = self.create_app_image(user, appname, manifest)
        except:
            pass
        else:
            # we were all successful, record in DB
            app = {
                'name' : appname,
                'git' : gituri,
                'docker' : dockerid,
                'manifest' : manifest
            }
            _, db = self.get_db()
            db.apps.insert(app)
            
    # internal methods
    def get_db(self):
        # get mongodb
        client = MongoClient(settings.DB_URL) 
        db = client.minicf
        return client, db
        
    def create_git(self, user, appname):
        """
        create a new bare repository at path GIT_HOME/user/appname.git
        this git can be directly used by git: 
        
        $ git git@server:/GIT_HOME/user/appname.git
        """
        path = self.gitpath(user, appname)
        assert not os.path.isdir(path)
        mkdir('-p', path)
        with cd(path):
            git('--bare', 'init')
        return self.gituri(user, appname)
    
    def create_buildpack_image(self, buildpack):
        """
        create a docker image for the buildpack 
        """ 
        with cd(settings.BIN_DIR):
            local('build-image %s %s' % (buildpack, buildpack))
            
    def create_combined_image(self, image, buildpacks):
        """
        create a combined image for several buildpacks
        """
        with cd(settings.BIN_DIR):
            local('build-image %s %s' % (image, " ".join(buildpacks)))
                    
    def create_app_image(self, user, appname, manifest):
        """
        create a docker image for the app 
        """ 
        print "hello"
        app = '%s/%s' % (user, appname)
        with cd(settings.BIN_DIR):
            local('build-app %s %s' % (app, 'stack/django'))
        
                
    def gituri(self, user, appname):
        """
        return the git uri of a particular app
        """
        return 'git@%s:/%s/%s/%s.git' % (hostname(),
                                         settings.GIT_HOME,
                                         user,
                                         appname)
    
    def gitpath(self, user, appname):
        """
        return the (local) path to the git repository for appname
        """
        return '%s/%s/%s.git' % (settings.GIT_HOME, user, appname)
           
     
            
            
            
        
        
        

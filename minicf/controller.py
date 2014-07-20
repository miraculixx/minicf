'''
Created on Jul 13, 2014

@author: patrick
'''
from fabric.operations import local
from minicf.models.app import App
from minicf.models.service import Service
from minicf.shutil import sh, mkdir, cd, git
from minimongo.options import configure
from pymongo.mongo_client import MongoClient
import docker
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
    def __init__(self):
        self.docker = docker.Client(base_url='unix://var/run/docker.sock',
                                    version='1.10',
                                    timeout=10)
    
    # public methods
    def login(self, user, password):
        """
        login the user onto the service
        """
        self.user = 'demo'
        return True 
    
    def register_app(self, user, appname, manifest=None):
        """
        register a new app. this is called by the push command
        and will do the following:
        
        1. setup a new git repository for this app
        2. register the repository and the app in the db
        
        @param appname the name of the app
        @manifest manifest the parsed manifest YML   
        """
        gitpath = self.create_git(user, appname)
        # record in DB
        app = self.get_or_create_app(user, appname, manifest)
        app.git = self.gituri(user, appname)
        app.save()
        return app
    
    def remove_app(self, user, appname):
        """
        remove the app, it's images and containers, as well
        as the git repository for good
        """
        app = self.check_app_valid(user, appname)
        # remove git
        local('rm -rf %s' % self.gitpath(user, appname))
        # remove docker containers
        img = self.imagename(user, appname)
        containers = self.docker.containers(all=True)
        for c in containers:
            if c.get('name', '__unknown__') == img:
                self.docker.remove_container(c['Id'])
        # remove docker image for app
        self.docker.remove_image(img)
        # delete app from db
        app.remove()
        
    def create_service(self, user, servicename, servicetype):
        """
        create a new service image:
        
        1. create the service image
        2. register in repository
        """
        serviceid = "%s/%s" % (user, servicename)
        service = Service.collection.find_one({'user' : user, 'name' : servicename})
        if not service:
            self.create_service_image(user, servicename, servicetype)
            service = Service({
                'user' : user,
                'name' : servicename
            })
            service.save()
        else:
            raise Exception('service %s already exists' % servicename)
        return service
        
    def remove_service(self, user, servicename):
        """
        remove the service, its containers and its images
        """
        service = self.check_service_valid(user, servicename)
        # remove docker containers
        img = self.imagename(user, servicename)
        containers = self.docker.containers(all=True)
        for c in containers:
            if c.get('name', '__unknown__') == img:
                self.docker.remove_container(c['Id'])
        # remove docker image for service
        self.docker.remove_image(img)
        # delete service from db
        service.remove()
            
    # internal methods
    def get_db(self):
        """
        get the registry database
        """
        # get mongodb
        client = MongoClient(settings.DB_URL) 
        db = client.minicf
        return client, db
    
    def get_or_create_app(self, user=None, appname=None, manifest=None):
        """
        get or create an app instance in the db
        """
        query = { 'user' : user, 'name' : appname }
        app = App.collection.find_one(query)
        if not app:
            app = App({
                'user' : user,
                'name' : appname,
                'git' : None,
                'docker' : None,
                'manifest' : manifest,
            })
            app.save()  
        return app
        
    def create_git(self, user, appname):
        """
        create a new bare repository at path GIT_HOME/user/appname.git
        this git can be directly used by git: 
        
        $ git git@server:/GIT_HOME/user/appname.git
        
        This will also record the gituri as part of the app in the DB
        """
        path = self.gitpath(user, appname)
        assert not os.path.isdir(path)
        mkdir('-p', path)
        with cd(path):
            git('--bare', 'init')
        return path
    
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
        manifest = manifest or settings.DEFAULT_MANIFEST 
        self.check_app_valid(user, appname)
        # if app is valid, build it 
        app = '%s/%s' % (user, appname)
        with cd(settings.BIN_DIR):
            local('build-app %s %s' % (app, manifest['framework']))
        return app
    
    def check_app_valid(self, user, appname):
        """
        retrieve app instance from repository, if valid
        """
        # get app from collection 
        app = App.collection.find_one({'user' : user, 'name' : appname})
        if not app:
            raise Exception('app is unknown')
        return app
    
    def check_service_valid(self, user, servicename):
        """
        retrieve service instance from repository, if valid
        """
        # get service from collection 
        service = Service.collection.find_one({'user' : user, 'name' : servicename})
        if not service:
            raise Exception('service is unknown')
        return service
    
    def create_service_image(self, user, servicename, servicetype):
        """
        create a new service image user/servicename. There must be
        a baseimage of name service/servicetype in order to build
        the service image.
        
        @param user the user name
        @param servicename the name of the service in user realm
        @param servicetype the name of the service (e.g. mysql) 
        """
        # create service
        image = self.imagename(user, servicename) 
        with cd(settings.BIN_DIR):
            baseimage = 'service/%s' % servicetype
            local('build-service %s %s' % (image, baseimage))
        return image
        
    def run_service(self, user, servicename):
        image = self.imagename(user, servicename)
        
                
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
    
    def imagename(self, user, appname):
        """
        return the docker image name as user/appname
        """
        return "%s/%s" % (user, appname)

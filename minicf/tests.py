'''
Created on Jul 13, 2014

@author: patrick
'''
from controller import MiniCFController
from minicf.models import App
from minicf.shutil import rm
from minimongo.options import configure
from pymongo.mongo_client import MongoClient
from unittest.case import TestCase
import os
import settings

class MiniCFControllerTests(TestCase):
    def setUp(self):
        # drop the database before we run the test
        client = MongoClient()
        client.drop_database(settings.MONGODB_DATABASE)
        
    def tearDown(self):
        pass
    
    def test_create_git(self):
        """
        test setup of git works correctly
        """
        path = '%s/testuser/sampleapp.git' % settings.GIT_HOME
        cleanUp(path)
        ctl = MiniCFController()
        ctl.create_git('testuser', 'sampleapp')
        self.assertTrue(os.path.isdir(path))
        # be nice and cleanup
        self.addCleanup(cleanUp, path)
        
    def test_app_model(self):
        """
        test the minimongo app model ORM
        """
        app = App({'name' : 'myapp'})
        app.save()
        self.assertIn('_id', app)
        self.assertIsNotNone(app._id, "expected _id not None")
        app = App.collection.find_one({'name' : 'myapp'})
        self.assertIn('_id', app)
        self.assertIsNotNone(app._id, "expected _id not None")
        
    def test_register_app(self):
        """
        test app registration
        """
        ctl = MiniCFController()
        path = '%s/testuser/sampleapp.git' % settings.GIT_HOME
        cleanUp(path)
        app = ctl.register_app('testuser', 'sampleapp')
        # check we have an actual app
        self.assertIn('_id', app)
        self.assertIsNotNone(app._id, "expected _id not None")
        # check the git repository was created
        self.assertTrue(os.path.isdir(path))
        # be nice and cleanup
        self.addCleanup(cleanUp, path)
        
    def test_check_app_valid(self):
        """
        test app validation
        """
        ctl = MiniCFController()
        path = '%s/testuser/sampleapp.git' % settings.GIT_HOME
        cleanUp(path)
        # case 1: no app known, should raise an exception
        def check_app_valid(user, appname,):
            app = ctl.check_app_valid(user, appname)
            print app
            print app.database
        self.assertRaises(Exception, check_app_valid, 'testuser', 'sampleapp')
        # case 2: app known, should return the app model instance
        ctl.register_app('testuser', 'sampleapp')
        app = ctl.check_app_valid('testuser', 'sampleapp')
        self.assertIn('_id', app)
        # be nice and cleanup
        self.addCleanup(cleanUp, ctl.gituri('testuser', 'sampleapp'))
        
    def test_remove_app(self):
        ctl = MiniCFController()
        path = '%s/testuser/sampleapp.git' % settings.GIT_HOME
        cleanUp(path)
        # create an app
        app = ctl.register_app('testuser', 'sampleapp')
        self.assertIn('_id', app)
        # create an image
        manifest = {'framework' : 'stack/minicf'}
        ctl.create_app_image('testuser', 'sampleapp', manifest)
        # remove app and image
        ctl.remove_app('testuser', 'sampleapp')
        self.assertFalse(os.path.isdir(path))
        # check there are no docker images left 
        containers = [c for c in ctl.docker.containers(all=True) \
           if c['Id']=='testuser/sampleapp']
        self.assertEqual(len(containers), 0)
        # be nice and cleanup
        self.addCleanup(cleanUp, ctl.gituri('testuser', 'sampleapp'))
        
    def test_create_service_image(self):
        user = 'testuser'
        servicename = 'mysqldb'
        servicetype = 'mysql'
        imagename = '%s/%s' % (user, servicename)
        ctl = MiniCFController()
        ctl.create_service_image(user, servicename, servicetype)
        # check the docker image is there
        images = ctl.docker.images(name=imagename)
        self.assertTrue(len(images) > 0)
        # cleanup
        ctl.docker.remove_image(imagename)
        
    def test_create_service(self):
        ctl = MiniCFController()
        user ='testuser'
        servicename = 'mysqldb'
        servicetype = 'mysql'
        # create the service
        service = ctl.create_service(user, servicename, servicetype)
        self.assertIn('_id', service)
        self.assertIsNotNone(service._id)
        # remove the service and images
        ctl.remove_service(user, servicename)
        # check there are no docker images left 
        containers = [c for c in ctl.docker.containers(all=True) \
           if c['Id'] == '%s/%s' % (user, servicename)]
        self.assertEqual(len(containers), 0)
        
    def test_remove_service(self):
        ctl = MiniCFController()
        user ='testuser'
        servicename = 'mysqldb'
        servicetype = 'mysql'
        # create the service
        service = ctl.create_service(user, servicename, servicetype)
        self.assertIn('_id', service)
        # remove the service and images
        ctl.remove_service(user, servicename)
        # check there are no docker images left 
        containers = [c for c in ctl.docker.containers(all=True) \
           if c['Id'] == '%s/%s' % (user, servicename)]
        self.assertEqual(len(containers), 0)
        
def cleanUp(path):
    if os.path.isdir(path):
        rm('-rf', path)
        
        
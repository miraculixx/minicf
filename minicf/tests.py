'''
Created on Jul 13, 2014

@author: patrick
'''
from controller import MiniCFController
from minicf.shutil import rm
from unittest.case import TestCase
import os
import settings


# change test settings
settings.GIT_HOME='/tmp/git'

class MiniCFControllerTests(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_create_git(self):
        """
        test setup of git works correctly
        """
        path = '%s/testuser/sampleapp.git' % settings.GIT_HOME
        def cleanUp():
            if os.path.isdir(path):
                rm('-rf', path)
        cleanUp()
        ctl = MiniCFController()
        ctl.create_git('testuser', 'sampleapp')
        self.assertTrue(os.path.isdir(path))
        # be nice and cleanup
        self.addCleanup(cleanUp)
        
        
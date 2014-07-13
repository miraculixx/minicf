'''
Created on Jul 13, 2014

@author: patrick
'''
import os
import sh as _sh

"""
a hack to avoid PyDev import error for sh
use as e.g. git = sh('git') or sh('git') 
"""
def sh(cmd=None):
    if cmd:
        return getattr(_sh, cmd)
    else:
        return _sh 

# setup some commands
mkdir = sh('mkdir')
git = sh('git')
rm = sh('rm')
rmdir = sh('rmdir')

#some other commands
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = newPath

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
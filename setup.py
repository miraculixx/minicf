'''
Created on Jul 14, 2014

@author: patrick
'''
from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
   name = "minicf",
   version = '0.0.1',
   author = 'Patrick Senti',
   author_email = 'ps@novapp.ch',
   description = 'A docker PaaS cloud using cloudfoundry concepts',
   license = 'MIT',
   packages = find_packages(),
   long_description=read('README'),
)
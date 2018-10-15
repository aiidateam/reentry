# -*- coding: utf8 -*-
"""
Install configuration for setuptools / pip
"""
from os import path
from setuptools import setup, find_packages
import json

README_PATH = path.join(path.dirname(path.abspath(__file__)), 'README.rst')

# Provide static information in setup.json
# such that it can be discovered automatically
with open('setup.json', 'r') as info:
    kwargs = json.load(info)
setup(packages=find_packages(), long_description=open(README_PATH).read(), long_description_content_type='text/x-rst', **kwargs)

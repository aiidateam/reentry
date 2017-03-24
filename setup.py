# -*- coding: utf8 -*-
from setuptools import setup, find_packages

if __name__=='__main__':
    setup(
        name = 'sparkplug',
        version = '0.1',
        author = 'Rico Häuselmann',
        packages = find_packages(),
        entry_points={
            'distutils.setup_keywords': [
                'spark_register = sparkplug.register:register_dist'
            ]
        }
    )

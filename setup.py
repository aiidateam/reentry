# -*- coding: utf8 -*-
from setuptools import setup, find_packages

if __name__=='__main__':
    setup(
        name = 'reentry',
        version = '0.1',
        author = 'Rico Häuselmann',
        packages = find_packages(),
        include_package_data=True,
        package_data={
            '': ['js_data']
        },
        entry_points={
            'distutils.setup_keywords': [
                'reentry_register = reentry.register:register_dist'
            ],
            'console_scripts': [
                'reentry = reentry.cli:reentry'
            ]
        }
    )

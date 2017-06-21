# -*- coding: utf8 -*-
from os import path
from setuptools import setup, find_packages

readmepath = path.join(path.dirname(path.abspath(__file__)), 'README.rst')
with open(readmepath, 'r') as readme:
    long_desc = readme.read()

setup(
    name = 'reentry',
    version = '1.0.2',
    author = 'Rico Häuselmann',
    license = 'MIT License',
    description='A plugin manager based on setuptools entry points mechanism',
    long_description=long_desc,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['js_data', 'README.rst']
    },
    entry_points={
        'distutils.setup_keywords': [
            'reentry_register = reentry.hooks:register_dist',
            'reentry_scan = reentry.hooks:scan'
        ],
        'console_scripts': [
            'reentry = reentry.cli:reentry'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Topic :: Software Development'
    ],
    install_requires={
        'setuptools >= 18.5',
        'click'
    }
)

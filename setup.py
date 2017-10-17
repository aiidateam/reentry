# -*- coding: utf8 -*-
"""
Install configuration for setuptools / pip
"""
from os import path
from setuptools import setup, find_packages

README_PATH = path.join(path.dirname(path.abspath(__file__)), 'README.rst')
with open(README_PATH, 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setup(
    name='reentry',
    version='1.0.2',
    author='Rico Häuselmann',
    license='MIT License',
    description='A plugin manager based on setuptools entry points mechanism',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['js_data', 'README.rst']},
    entry_points={
        'distutils.setup_keywords': ['reentry_register = reentry.hooks:register_dist', 'reentry_scan = reentry.hooks:scan'],
        'console_scripts': ['reentry = reentry.cli:reentry'],
        'test_entry_points': ['test = reentry.cli:reentry']
    },
    classifiers=[
        'License :: OSI Approved :: MIT License', 'Programming Language :: Python', 'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins', 'Intended Audience :: Developers', 'Topic :: Software Development'
    ],
    install_requires={'setuptools >= 18.5', 'click', 'six'},
    extras_require={
        'dev': [
            'pre-commit',
            'prospector',
            'pylint',
            'flake8',
            'pytest',
            'yapf',
            'coverage',
            'pytest-cov',
            'tox'
        ]
    })

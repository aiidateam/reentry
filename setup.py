# -*- coding: utf8 -*-
"""
Install configuration for setuptools / pip
"""
from os import path
from setuptools import setup, find_packages

README_PATH = path.join(path.dirname(path.abspath(__file__)), 'README.rst')
with open(README_PATH, 'r') as readme:
    LONG_DESCRIPTION = readme.read()

VERSION = '1.2.1'

setup(
    name='reentry',
    version=VERSION,
    author='Rico Haeuselmann',
    license='MIT License',
    description='A plugin manager based on setuptools entry points mechanism',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['js_data', 'README.rst']},
    entry_points={
        'distutils.setup_keywords': ['reentry_register = reentry.hooks:register_dist', 'reentry_scan = reentry.hooks:scan_for_installed'],
        'console_scripts': ['reentry = reentry.cli:reentry'],
        'test_entry_points': ['test = reentry.cli:reentry']
    },
    classifiers=[
        'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable', 'Environment :: Plugins', 'Intended Audience :: Developers',
        'Topic :: Software Development'
    ],
    install_requires=['setuptools >= 36.2', 'click', 'six', 'pathlib2 ; python_version<"3.5"'],
    extras_require={
        'dev': ['pre-commit', 'prospector', 'pylint', 'flake8', 'pytest', 'yapf', 'coverage', 'pytest-cov', 'tox', 'packaging']
    })

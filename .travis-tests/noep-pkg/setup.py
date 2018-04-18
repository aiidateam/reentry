# pylint: disable=missing-docstring
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(name='reentry-test-noep', packages=find_packages(), setup_requires=['reentry==1.2.0a9'], reentry_register=True)

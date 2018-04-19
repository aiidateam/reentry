# pylint: disable=missing-docstring
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(name='reentry-test-noep', packages=find_packages(), reentry_register=True)

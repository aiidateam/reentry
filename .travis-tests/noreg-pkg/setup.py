# pylint: disable=missing-docstring
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(name='reentry-test-noreg',
          packages=find_packages(),
          entry_points={'reentry_test': ['test-noreg = reentry_test_plugin.plugin:PluginClass']})

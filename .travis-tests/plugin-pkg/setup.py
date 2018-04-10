# pylint: disable=missing-docstring
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='reentry-test-plugin',
        packages=find_packages(),
        install_requires=['reentry'],
        reentry_register=True,
        entry_points={
            'reentry_test': ['test-plugin = reentry_test_plugin.plugin:PluginClass']
        })

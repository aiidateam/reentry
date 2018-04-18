# pylint: disable=missing-docstring
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='reentry-test-host',
        packages=find_packages(),
        setup_requires=['reentry==1.2.0a6'],
        install_requires=['reentry==1.2.0a6'],
        reentry_scan=['reentry_test'],
        reentry_register=True,
        entry_points={
            'console_scripts': ['reentry-test-hooks = reentry_test_host.tests:main'],
            'reentry_test': ['builtin = reentry_test_host.builtin:PluginClass']
        })

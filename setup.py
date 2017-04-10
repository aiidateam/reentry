# -*- coding: utf8 -*-
from setuptools import setup, find_packages

if __name__ == ' __main__':
    setup(
        name = 'reentry',
        version = '0.9',
        author = 'Rico Häuselmann',
        license = 'MIT License',
        packages = find_packages(),
        include_package_data=True,
        package_data={
            '': ['js_data']
        },
        entry_points={
            'distutils.setup_keywords': [
                'reentry_register = reentry.hooks:register_dist'
            ],
            'console_scripts': [
                'reentry = reentry.cli:reentry'
            ]
        },
        install_requires=[
            'click',

        ],
 	classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Topic :: Software Development'
        ]
    )

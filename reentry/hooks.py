# -*- coding: utf8 -*-
"""
Define a setuptools extension.


Host usage::

    setup(
        ...,
        reentry_scan=['group1', 'group2'],
        ...
    )

Plugin usage::

    setup(
        ...,
        reentry_register = True,
        ...
    )
"""
from __future__ import print_function


def is_bool(value):
    """Return True if `value` is a boolean."""
    return bool(value) == value


def register_dist(dist, attr, value):
    """If value is True, register the distribution's entry points in reentrys storage."""
    from distutils.errors import DistutilsSetupError  # pylint: disable=import-error,no-name-in-module
    # assert is boolean
    if not is_bool(value):
        raise DistutilsSetupError('{} must be a boolean, got {}'.format(attr, value))

    if value:
        print('registering entry points with reentry...')
        from reentry import manager
        # ~ print('\n'.join(['{} = {}'.format(k, v) for k, v in dist.__dict__.items()]))
        manager.register(dist)


def ensure_list(value, attr):
    """raise an error if `value` is not a list"""
    from distutils.errors import DistutilsSetupError  # pylint: disable=import-error,no-name-in-module
    if not isinstance(value, list):
        raise DistutilsSetupError('{} must be a list, got {}'.format(attr, value.__class__))


def scan_for_installed(dist, attr, value):  # pylint: disable=unused-argument
    """
    scan for entry points of the given groups in the already installed
    distributions

    :param value: a list of groups names to scan for
    """
    ensure_list(value, attr)
    if value:
        print('scanning for plugins...')
        from reentry import manager
        manager.scan(groups=value, group_re=False)
        print('... done.')

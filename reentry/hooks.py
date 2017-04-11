# -*- coding: utf8 -*-
"""
define a setuptools extension
"""
from __future__ import print_function


def is_bool(value):
    """return True if `value` is a boolean"""
    return bool(value) == value


def register_dist(dist, attr, value):
    """
    if value is True, register the distribution's entry points in
    reentrys storage
    """
    from distutils.errors import DistutilsSetupError
    '''assert is boolean'''
    if not is_bool(value):
        raise DistutilsSetupError(
            '{} must be a boolean, got {}'.format(attr, value)
        )

    if value:
        print('registering entry points with reentry...')
        from reentry.jsonbackend import JsonBackend
        jb = JsonBackend()
        jb.write_st_dist(dist)


def ensure_list(value, attr):
    """raise an error if `value` is not a list"""
    from distutils.errors import DistutilsSetupError
    if not isinstance(value, list):
        raise DistutilsSetupError(
            '{} must be a list, got {}'.format(attr, value.__class__))


def scan_for_installed(dist, attr, value):
    """
    scan for entry points of the given groups in the already installed
    distributions

    :param value: a list of groups names to scan for
    """
    ensure_list(value, attr)
    if value:
        print('scanning for plugins...')
        from reentry.manager import scan
        scan(value, group_re=False)

# -*- coding: utf8 -*-
"""
define a setuptools extension
"""
from __future__ import print_function

def is_bool(value):
    return bool(value) == value


def register_dist(dist, attr, value):
    """
    if value is True, register the distribution's entry points in
    reentrys storage
    """
    print(dist.get_name())
    '''assert is boolean'''
    if not is_bool(value):
        raise DistutilsSetupError(
            '{} must be a boolean, got {}'.format(attr, value)
        )

    if value:
        from reentry.jsonbackend import JsonBackend
        jb = JsonBackend()
        jb.write_st_dist(dist)

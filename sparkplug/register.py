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
    sparkplugs storage
    """
    # TODO: this is for debugging and will have to go in production
    from pprint import pprint
    print(dist.get_name())
    '''assert is boolean'''
    if not is_bool(value):
        raise DistutilsSetupError(
            '{} must be a boolean, got {}'.format(attr, value)
        )

    if value:
        from sparkplug.jsonbackend import JsonBackend
        jb = JsonBackend()
        jb.write_st_dist(dist)
        # TODO: this is for debugging and will have to go in production
        print(jb.get_dist_map(dist.get_name()))

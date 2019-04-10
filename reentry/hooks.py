# -*- coding: utf8 -*-
"""
Define a setuptools extension.

Usage::

    setup(
        ...,
        reentry_register = True,
        ...
    )
"""
from __future__ import print_function
import sys

from reentry.config import get_datafile


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
        print('[ REENTRY ] registering entry points with reentry...', file=sys.stderr)
        from reentry import manager
        dist_name, entry_point_map = manager.register(dist)
        print('[ REENTRY ] ... registered to {}'.format(get_datafile()), file=sys.stderr)
        print('[ REENTRY ] Following entrypoints were registered\n', file=sys.stderr)
        print(manager.format_map({dist_name: entry_point_map}), file=sys.stderr)
        print('[ REENTRY ] Current entry point map at {}:'.format(get_datafile()), file=sys.stderr)
        print(manager.format_map(manager.get_dist_map()), file=sys.stderr)


def ensure_list(value, attr):
    """raise an error if `value` is not a list"""
    from distutils.errors import DistutilsSetupError  # pylint: disable=import-error,no-name-in-module
    if not isinstance(value, list):
        raise DistutilsSetupError('{} must be a list, got {}'.format(attr, value.__class__))

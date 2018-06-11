# -*- coding: utf8 -*-
"""Manager for entry point based plugins. Main client facing API"""
from __future__ import print_function
import re

import six

from reentry.jsonbackend import JsonBackend

__all__ = ['PluginManager', 'get_default_backend', 'DEFAULT_MANAGER']

IGNORE_BY_DEFAULT = {
    'console_scripts', 'gui_scripts', 'distutils.commands', 'distutils.setup_keywords', 'setuptools.installation',
    'setuptools.file_finders', 'egg_info.writers'
}


def clean_map(entry_point_map, exceptions=None):
    """Extract entry points that are clearly not for plugins unless excepted."""
    ep_map = entry_point_map.copy()
    ignore_set = IGNORE_BY_DEFAULT.difference(set(exceptions or []))
    for ignore_group in ignore_set:
        ep_map.pop(ignore_group, None)
    return ep_map


def get_default_backend():
    from reentry.config import get_datafile
    return JsonBackend(datafile=get_datafile())


class PluginManager(object):
    """Manage a set of cached entry points"""

    def __init__(self, backend=get_default_backend(), scan_for_not_found=True):
        self._backend = backend
        self._scan_for_not_found = scan_for_not_found

    def iter_entry_points(self, group, name=None):
        """
        Iterate over all registered entry points in `group`, or if `name` is given, only the ones matching `name`.

        If no entry point (or none called `name`), a scan is triggered, which may take a while. This behaviour can be configured when
        creating the plugin manager.

        The backend may only load pkg_resources if any of the entry points contain extras requirements
        """
        if self._scan_for_not_found:
            if not self.get_entry_map(groups=[group]):
                self.scan(groups=[group])
            elif name and name not in self.get_entry_map(groups=[group], ep_names=[name]).get(group, {}).keys():
                self.scan(groups=[group])
        for entry_point in self._backend.iter_group(group):
            if name:
                if name in entry_point.name:
                    yield entry_point
            else:
                yield entry_point

    def get_entry_map(self, dist_names=None, groups=None, ep_names=None):
        """
        return the entry point map for `group` or the whole map for `dist`

        The backend may only load pkg_resources if any of the entry points contain extras requirements
        """
        return self._backend.get_map(dist=dist_names, group=groups, name=ep_names)

    def get_dist_map(self, dist=None):
        """Get a map of entry points sorted by distribution."""
        return self._backend.get_dist_map(dist=dist)

    @staticmethod
    def format_map(entry_point_map, indent=1):
        tabs = '\t' * indent
        newl = '\n' + tabs
        return tabs + newl.join(['{} -> {}'.format(dname, dmap) for dname, dmap in entry_point_map.items()])

    def register(self, distribution):
        """
        Registers the distribution's entry points with the backend.

        The backend may load pkg_resources to resolve the distribution name

        Takes either a string or a Distribution object as passed by setuptools to hooks during install.
        """
        dist_name, entry_point_map = self._backend.scan_dist(distribution)
        entry_point_map = clean_map(entry_point_map)
        self._backend.write_dist_map(dist_name, entry_point_map)
        return dist_name, entry_point_map

    def scan(self, groups=None, group_re=None, nocommit=False, nodelete=False):
        """Walk through all distributions available and registers entry points or only those in `groups`."""
        import pkg_resources as pr
        pr_env = pr.AvailableDistributions()
        pr_env.scan()
        if not groups and group_re:
            groups = []

        if group_re:
            if isinstance(group_re, six.string_types):
                group_re = re.compile(group_re)
            all_groups = self.scan_all_group_names()
            groups.extend({group for group in all_groups if group_re.match(group)})

        if not nocommit and not nodelete:
            if groups:
                for group in groups:
                    self._backend.rm_group(group)
            else:
                self._backend.clear()

        full_map = {}

        if nodelete:
            full_map = self._backend.epmap.copy()

        # ~ for dists in pr_env._distmap.values():  # pylint: disable=protected-access
        for dist in pr_env:
            dname, emap = self._backend.scan_dist(dist)
            dmap = full_map.get(dname, {})
            if groups:
                new_dmap = {k: v for k, v in six.iteritems(emap) if k in groups}
                dmap.update(new_dmap)
            else:
                dmap.update(emap)

            # extract entry points that are reserved for other purposes unless excepted
            dmap = clean_map(dmap, exceptions=groups)

            if not nocommit:
                self._backend.write_dist_map(dname, entry_point_map=dmap)
            full_map[dname] = [dmap]

        return full_map

    def scan_all_group_names(self):
        """Use `pkg_resources` to get a set of all available (not only cached) groups."""
        import pkg_resources as pr
        pr_env = pr.AvailableDistributions()
        pr_env.scan()
        all_groups = set()
        for dist_name in pr_env:
            _, dmap = self._backend.scan_dist(dist_name)
            all_groups.update(dmap.keys())
        return all_groups

    def unregister(self, distname):
        """
        unregisters the distribution's entry points with the backend

        The backend may load pkg_resources to resolve the distribution name
        """
        self._backend.rm_dist(distname)

    @property
    def distribution_names(self):
        return self._backend.get_dist_names()


DEFAULT_MANAGER = PluginManager()

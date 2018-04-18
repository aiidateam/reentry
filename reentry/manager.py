# -*- coding: utf8 -*-
"""Manager for entry point based plugins. Main client facing API"""
from __future__ import print_function
import six

from reentry.jsonbackend import JsonBackend

__all__ = ['PluginManager', 'get_default_backend', 'DEFAULT_MANAGER']


def get_default_backend():
    from reentry.config import get_datafile
    return JsonBackend(datafile=get_datafile())


class PluginManager(object):
    """Manage a set of cached entry points"""

    def __init__(self, backend=get_default_backend()):
        self._backend = backend

    def iter_entry_points(self, group, name=None):
        """
        returns all registered entry points in `group`, or if `name` is given,
        only the ones matching `name`.

        The backend may only load pkg_resources if any of the entry points contain extras requirements
        """
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

    @staticmethod
    def format_map(entry_point_map):
        return '\n'.join(['{} -> {}'.format(dname, dmap) for dname, dmap in entry_point_map.items()])

    def register(self, distribution):
        """
        Registers the distribution's entry points with the backend.

        The backend may load pkg_resources to resolve the distribution name

        Takes either a string or a Distribution object as passed by setuptools to hooks during install.
        """
        if isinstance(distribution, six.string_types):
            dist_name, entry_point_map = self._backend.write_st_dist(distribution)
        else:
            dist_name, entry_point_map = self._backend.write_install_dist(distribution)
        return dist_name, entry_point_map

    def scan(self, groups=None, group_re=None, nocommit=False, nodelete=False):
        """
        walks through all distributions available and registers entry points or only those in `groups`
        """
        import pkg_resources as pr
        pr_env = pr.AvailableDistributions()
        pr_env.scan()
        if not groups and group_re:
            groups = []

        if group_re:
            groups.extend({group for group in self._backend.get_group_names() if group_re.match(group)})

        if not nocommit and nodelete:
            if groups:
                for group in groups:
                    self._backend.rm_group(group)
            else:
                self._backend.clear()

        full_map = {}

        if nodelete:
            full_map = self._backend.ep_map()

        for dists in pr_env._distmap.values():  # pylint: disable=protected-access
            dist = dists[0]
            emap = dist.get_entry_map() or {}
            dname = dist.project_name
            dmap = full_map.get(dname, {})
            if groups:
                new_dmap = {k: v for k, v in six.iteritems(emap) if k in groups}
                dmap.update(new_dmap)
            else:
                dmap.update(emap)
            if not nocommit:
                self._backend.write_dist_map(dname, entry_point_map=dmap)
            full_map[dname] = [dmap]

        return full_map

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

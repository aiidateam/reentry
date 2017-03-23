# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod


class BackendInterface(object):
    __metaclass__ = ABCMeta
    """
    Backend interface
    """
    def get_map(self, dist=None, group=None, name=None):
        """
        get a map of entry points, filtered by

        :param dist: single distribution name or sequence of distribution names
        :param groups: single group name or sequence of group names
        :param name: entry point name or sequence of names

        The map is structured as follows::

            map = {
                'group': {
                    'dist': [
                        'entry.point',
                        ...
                    ],
                    ...
                },
                ...
            }
        """

    def iter_group(self, group):
        """
        returns a list of entry points for the given group name
        """

    def get_group_names(self):
        """
        returns a list of group names
        """

    def get_dist_names(self):
        """
        returns a list of distribution names
        """

    def get_dist_map(self, dist):
        """
        returns a map {group:[entry_points, ...], ...} for the given dist name
        """

    def write_dist(self, dist):
        """
        add a distribution, empty by default
        """

    def rm_dist(self, distname):
        """
        removes a distribution completely
        """

    def pr_dist_map(self, distname):
        from pkg_resources import get_distribution
        dist = get_distribution(distname)
        dname = dist.project_name
        epmap = dist.get_entry_map()
        return dname, epmap

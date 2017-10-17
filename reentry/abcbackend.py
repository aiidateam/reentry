# -*- coding: utf8 -*-
"""Abstract base class for backends"""
from abc import ABCMeta


class BackendInterface(object):
    """
    Backend interface, subclass to implement a concrete backend.


    All methods without a method body need to be implemented in a backend.
    """
    __metaclass__ = ABCMeta

    def get_map(self, dist=None, group=None, name=None):
        """
        get a map of entry points, filtered by

        :param dist: distribution name or sequence of distribution names
        :param groups: single group name or sequence of group names
        :param name: entry point name pattern or sequence of name patterns

        The map is structured as follows::

            map = {
                    '<group>': {
                        '<entrypoint name>: <EntryPoint instance>
                        ...
                    },
                    ...
                },
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

    def write_pr_dist(self, dist):
        """
        add a distribution, empty by default
        """

    def write_st_dist(self, dist):
        """
        add a distribution during it's installation
        """

    def write_dist(self, distname, entry_point_map=None):
        """
        take a distribution's project name, add the distribution
        """
        if entry_point_map:
            self.write_dist_map(distname=distname, entry_point_map=entry_point_map)
        else:
            dist = self.pr_dist_from_name(distname)
            self.write_pr_dist(dist)

    def write_dist_map(self, distname, entry_point_map=None):
        """Write a distribution given the name and entry point map"""

    def rm_dist(self, distname):
        """
        removes a distribution completely
        """

    def clear(self):
        """Clears all stored entry points"""

    @staticmethod
    def pr_dist_map(dist):
        dname = dist.project_name
        epmap = dist.get_entry_map()
        return dname, epmap

    @staticmethod
    def pr_dist_from_name(distname):
        from pkg_resources import get_distribution
        dist = get_distribution(distname)
        return dist

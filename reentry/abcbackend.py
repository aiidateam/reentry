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

        :param dist: distribution name
        :param groups: single group name or sequence of group names
        :param name: entry point name or sequence of names

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

    def write_dist(self, distname):
        """
        take a distribution's project name, add the distribution
        """
        dist = self.pr_dist_from_name(distname)
        self.write_pr_dist(dist)

    def rm_dist(self, distname):
        """
        removes a distribution completely
        """

    def pr_dist_map(self, dist):
        dname = dist.project_name
        epmap = dist.get_entry_map()
        return dname, epmap

    def pr_dist_from_name(self, distname):
        from pkg_resources import get_distribution
        dist = get_distribution(distname)
        return dist

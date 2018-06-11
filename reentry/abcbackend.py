# -*- coding: utf8 -*-
"""Abstract base class for backends"""
import abc
import six


class BackendInterface(object):
    """
    Backend interface, subclass to implement a concrete backend.


    All methods without a method body need to be implemented in a backend.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
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

    @abc.abstractmethod
    def iter_group(self, group):
        """
        returns a list of entry points for the given group name
        """

    @abc.abstractmethod
    def get_group_names(self):
        """
        returns a list of group names
        """

    @abc.abstractmethod
    def get_dist_names(self):
        """
        returns a list of distribution names
        """

    @abc.abstractmethod
    def get_dist_map(self, dist):
        """
        returns a map {group:[entry_points, ...], ...} for the given dist name
        """

    @abc.abstractmethod
    def scan_st_dist(self, dist):
        """Scan a distribution given by a name, empty by default."""

    @abc.abstractmethod
    def scan_install_dist(self, dist):
        """Add an incomplete distribution as passed by setuptools during it's installation."""

    def scan_dist(self, distribution):
        """
        take a distribution's project name, add the distribution
        """
        if isinstance(distribution, six.string_types):
            dist_name, entry_point_map = self.scan_st_dist(distribution)
        else:
            dist_name, entry_point_map = self.scan_install_dist(distribution)
        return dist_name, entry_point_map

    @abc.abstractmethod
    def write_dist_map(self, distname, entry_point_map=None):
        """Write a distribution given the name and entry point map"""

    @abc.abstractmethod
    def rm_dist(self, distname):
        """
        removes a distribution completely
        """

    @abc.abstractmethod
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

    @abc.abstractproperty
    def epmap(self):
        """Full map {distribution: {group: [{name: entry_point}]}}."""

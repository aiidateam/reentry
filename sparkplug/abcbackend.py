# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod


class BackendInterface(object):
    __metaclass__ = ABCMeta
    """
    Backend interface
    """
    @abstractmethod
    def get_map(self, dist=None, groups=None, name=None):
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

    @abstractmethod
    def get_group(self, group):
        """
        returns a list of entry points for the given group name
        """

    @abstractmethod
    def get_group_names(self):
        """
        returns a list of group names
        """

    @abstractmethod
    def get_dist_names(self):
        """
        returns a list of distribution names
        """

    @abstractmethod
    def get_dist(self, dist):
        """
        returns a map {group:[entry_points, ...], ...} for the given dist name
        """

    @abstractmethod
    def write_dist(self, dist):
        """
        add a distribution, empty by default
        """

    @abstractmethod
    def rm_dist(self, distname):
        """
        removes a distribution completely
        """

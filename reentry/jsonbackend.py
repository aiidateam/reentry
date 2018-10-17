# -*- coding: utf8 -*-
"""A backend that uses a json file to store entry points."""
import json

import six

from reentry.abcbackend import BackendInterface
from reentry.entrypoint import EntryPoint


class JsonBackend(BackendInterface):
    """
    Backend using json
    """

    def __init__(self, datafile=None):
        super(JsonBackend, self).__init__()
        from os.path import join, dirname, exists
        self.datafile = join(dirname(__file__), 'js_data')
        self.datafile = datafile or self.datafile
        if not exists(self.datafile):
            with open(self.datafile, 'w') as datafp:
                datafp.write('{}')
        self._epmap = self.read()

    @property
    def epmap(self):
        return self._epmap.copy()

    def read(self):
        """
        read state from storage
        """
        with open(self.datafile, 'r') as cache_file_obj:
            return json.load(cache_file_obj)

    def write(self):
        """
        write the current state to storage
        """
        with open(self.datafile, 'w') as cache_file_obj:
            json.dump(self._epmap, cache_file_obj)

    @staticmethod
    def scan_pr_dist(dist):
        """
        add a distribution, empty by default
        """
        dname = dist.project_name
        epmap = dist.get_entry_map()
        return dname, epmap

    def write_dist_map(self, distname, entry_point_map=None):
        dname = distname
        entry_point_map = {k: {kk: str(vv) for kk, vv in six.iteritems(v)} for k, v in six.iteritems(entry_point_map)}
        # update entry point storage
        # --> only if there is something to update though
        if entry_point_map:
            if not self._epmap.get(dname):
                self._epmap[dname] = {}
            self._epmap[dname].update(entry_point_map)
            self.write()

    def scan_st_dist(self, dist):
        """Add a distribution by name."""
        return self.scan_pr_dist(self.pr_dist_from_name(dist))

    def scan_install_dist(self, dist):
        """Add a distribution during it's install."""
        distname = dist.get_name()
        entrypoint_map = {}
        dist_map = {}
        if hasattr(dist, 'entry_points'):
            dist_map = dist.entry_points or {}
        for group, entrypoint_list in dist_map.items():
            entrypoint_map[group] = {}
            for entrypoint_string in entrypoint_list:
                entry_point = EntryPoint.parse(entrypoint_string)
                entrypoint_map[group][entry_point.name] = entrypoint_string
        return distname, entrypoint_map

    def iter_group(self, group):
        """Iterate over entry points within a given group."""
        for dist in self._epmap:
            for _, entry_point_spec in six.iteritems(self._epmap[dist].get(group, {})):
                yield EntryPoint.parse(entry_point_spec)

    def get_pr_dist_map(self, dist):
        return self.get_dist_map(dist.project_name)

    def get_dist_map(self, dist=None):
        """Return the entry map of a given distribution."""
        if not dist:
            return self._epmap.copy()
        dmap = self._epmap.get(dist, {}).copy()
        for gname in dmap:
            for epname in dmap[gname]:
                dmap[gname][epname] = EntryPoint.parse(dmap[gname][epname])
        return dmap

    def get_ep(self, group, name, dist=None):
        """
        Get an entry point.

        :param group: the group name
        :param name: the entry point name
        :param dist: if not given, search in all dists

        if no dist was given, and the search turned up more than one
        entry point with the same name, returns a list of entrypoints
        else, returns an entry point
        """
        if not dist:
            specs = []
            for dist_name in self._epmap.keys():
                spc = self.get_ep(group, name, dist=dist_name)
                if spc:
                    specs.append(spc)
            # pylint: disable=no-else-return
            if len(specs) > 1:
                return specs
            elif len(specs) == 1:
                return specs[0]

        distribution_map = self._epmap.get(dist, {})
        group_map = distribution_map.get(group, {})
        spec = group_map.get(name)
        if spec:
            return EntryPoint.parse(spec)

        return None

    def get_dist_names(self):
        """
        Returns a list of distribution names
        """
        return self._epmap.keys()

    def get_group_names(self):
        """
        Returns a list of group names
        """
        glist = []
        for dist in self.get_dist_names():
            glist.extend(self._epmap[dist].keys())

        return list(set(glist))

    def rm_dist(self, distname):
        """
        removes a distributions entry points from the storage
        """
        if distname in self.get_dist_names():
            self._epmap.pop(distname)
        self.write()

    def rm_group(self, group):
        """
        removes a group from all dists
        """
        for dist in self._epmap:
            self._epmap[dist].pop(group, None)
        self.write()

    def clear(self):
        """
        completely clear entry_point storage
        """
        self._epmap = {}
        self.write()

    def get_map(self, dist=None, group=None, name=None):
        """See BackendInterface docs."""
        # sanitize dist kwarg
        dist_list = self._dist_list_from_arg(dist)

        # sanitize groups kwarg
        group_list = self._group_list_from_arg(group)

        # sanitize name kwarg
        name_list = _listify(name)

        filtered_entry_points = self._filter_entry_points(dist_list, group_list, name_list)
        entry_point_map = {}
        for entry_point, ep_info in six.iteritems(filtered_entry_points):
            if not ep_info['group'] in entry_point_map:
                entry_point_map[ep_info['group']] = {}
            entry_point_map[ep_info['group']][ep_info['name']] = EntryPoint.parse(entry_point)

        return entry_point_map

    def _filter_groups_by_distribution(self, distribution_list, group_list=None):
        """List only groups (optionally from a given list of groups) registered for the given list of distributions"""
        if group_list is None:
            group_list = self.get_group_names()
        group_set = set()
        for distribution in distribution_list:
            if distribution not in self._epmap:
                raise ValueError("The {} distribution was not found.".format(distribution))
            else:
                group_set.update([group_name for group_name in self._epmap[distribution].keys() if group_name in group_list])
        return group_set

    def _filter_entry_points(self, dist_list, group_list, name_list):
        """
        Get a flat dict of annotated entry points, filtered by various criteria

        The dict is formatted like _flat_entry_points() output

        filter by::

            * dist_list: list of distribution names
            * group_list: list of group names
            * name_list: list of regex patterns for entry point names

        Example::

            >> backend.epmap

            {
                'A': {
                    'B': {'entry_point_C': 'entry_point_c = A.foo:bar'},
                    ...
                },
                'other_dist': {
                    'B': { ... },
                    ...
                },
                ...
            }

            >> backend._filter_entry_points(dist_list=['A'], group_list=['B'], name_list=['.*C.*'])

            {'B':
                {'entry_point_C': 'entry_point_c = A.foo:bar'}
            }

        """
        entry_points = self._flat_entry_points()

        def matches(entry_point):
            """True if the entry point matches the filters."""
            result = self._match_pattern_list_exact(entry_point['dist'], dist_list)
            result &= self._match_pattern_list_exact(entry_point['group'], group_list)
            result &= self._match_pattern_list_regex(entry_point['name'], name_list)
            return result

        return {k: v for k, v in six.iteritems(entry_points) if matches(v)}

    @staticmethod
    def _match_pattern_list_regex(name, pattern_list):
        """True if the entry point name matches one of a list of regex patterns."""
        import re
        if not pattern_list:
            return True
        return any([re.match(pattern, name) for pattern in pattern_list])

    @staticmethod
    def _match_pattern_list_exact(name, pattern_list):
        if not pattern_list:
            return True
        return bool(name in pattern_list)

    def _group_list_from_arg(self, group_arg):
        group_list = _listify(group_arg)
        if group_list is None:
            group_list = self.get_group_names()
        return group_list

    def _dist_list_from_arg(self, dist_arg):
        dist_list = _listify(dist_arg)
        if dist_list is None:
            dist_list = self.get_dist_names()
        return dist_list

    def _flat_entry_points(self):
        """Get a flat dict of entry points (keys) annotated with {name: .., group: .., dist: ..} (values)"""
        epflat = {}
        for distribution, dist_dict in six.iteritems(self._epmap):
            for group, group_dict in six.iteritems(dist_dict):
                for ep_name, entry_point in six.iteritems(group_dict):
                    epflat[entry_point] = {'name': ep_name, 'group': group, 'dist': distribution}
        return epflat


def _listify(sequence_or_name):
    """Wrap a single name in a list, leave sequences and None unchanged"""
    from collections import Sequence
    # pylint: disable=no-else-return
    if sequence_or_name is None:
        return None
    elif not isinstance(sequence_or_name, Sequence) or isinstance(sequence_or_name, six.string_types):
        return [sequence_or_name]
    return sequence_or_name

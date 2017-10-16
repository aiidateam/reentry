# -*- coding: utf8 -*-
"""Manager for entry point based plugins. Main client facing API"""
from reentry.jsonbackend import JsonBackend

DEFAULT_BACKEND = JsonBackend()


class PluginManager(object):
    """Manage a set of cached entry points"""

    def __init__(self, backend=DEFAULT_BACKEND):
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

    def register(self, distname):
        """
        registers the distribution's entry points with the backend

        The backend may load pkg_resources to resolve the distribution name
        """
        self._backend.write_dist(distname)

    def scan(self, groups=None, group_re=None):
        """
        walks through all distributions available and registers entry points or only those in `groups`
        """
        import pkg_resources as pr
        pr_env = pr.AvailableDistributions()
        pr_env.scan()
        if groups:
            for group in groups:
                self._backend.rm_group(group)
        else:
            self._backend.clear()

        for dists in pr_env._distmap.values():  # pylint: disable=protected-access
            dist = dists[0]
            emap = dist.get_entry_map()
            if groups:
                dmap = {k: v for k, v in emap.iteritems() if k in groups}
            elif group_re:
                dmap = {k: v for k, v in emap.iteritems() if group_re.match(k)}
            else:
                dmap = emap
            dname = dist.project_name
            self._backend.write_dist_map(dname, dmap)

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

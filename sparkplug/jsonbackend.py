# -*- coding: utf8 -*-
import json

from sparkplug.abcbackend import BackendInterface


class JsonBackend(BackendInterface):
    """
    Backend using json
    """
    def __init__(self):
        super(JsonBackend, self).__init__()
        from os.path import join, dirname, exists
        self.datafile = join(dirname(__file__), 'js_data')
        if not exists(self.datafile):
            with open(self.datafile, 'w') as datafp:
                datafp.write('{}')
        self.epmap = self.read()

    def read(self):
        """
        read state from storage
        """
        with open(self.datafile, 'r') as fp:
            return json.load(fp)

    def write(self):
        """
        write the current state to storage
        """
        with open(self.datafile, 'w') as fp:
            json.dump(self.epmap, fp)

    def write_dist(self, dist):
        """
        add a distribution, empty by default
        """
        dname, epmap = self.pr_dist_map(dist)
        if not self.epmap.get(dname):
            self.epmap[dname] = {}
        epmap = {k: {kk: str(vv) for kk, vv in v.iteritems()} for k, v in epmap.iteritems()}
        self.epmap[dname].update(epmap)
        self.write()

    def iter_group(self, group):
        """
        iterate over entry points within a given group
        """
        from sparkplug.entrypoint import EntryPoint
        for dist in self.epmap:
            for en, ep in self.epmap[dist].get(group, {}).iteritems():
                yield EntryPoint.parse(ep)

    def get_dist_map(self, distname):
        """
        return the entry map of a given distribution
        """
        from sparkplug.entrypoint import EntryPoint
        dmap = self.epmap.get(distname, {}).copy()
        for gname in dmap:
            for epname in dmap[gname]:
                dmap[gname][epname] = EntryPoint.parse(dmap[gname][epname])
        return dmap

    def get_ep(self, group, name, dist=None):
        """
        get an entry point

        :param group: the group name
        :param name: the entry point name
        :param dist: if not given, search in all dists

        if no dist was given, and the search turned up more than one
        entry point with the same name, returns a list of entrypoints
        else, returns an entry point
        """
        from sparkplug.entrypoint import EntryPoint
        if not dist:
            specs = []
            for dist in self.epmap.keys():
                spc = self.get_ep(group, name, dist=dist)
                spc and specs.append(spc)
            if len(specs) > 1:
                return specs
            elif len(specs) == 1:
                return specs[0]
        else:
            distm = self.epmap.get(dist, {})
            groupm = distm.get(group, {})
            spec = groupm.get(name)
            if spec:
                return EntryPoint.parse(spec)

    def get_dist_names(self):
        """
        returns a list of distribution names
        """
        return self.epmap.keys()

    def get_group_names(self):
        """
        returns a list of group names
        """
        glist = []
        for dist in self.get_dist_names():
            glist.extend(self.epmap[dist].keys())

        return list(set(glist))

    def rm_dist(self, distname):
        """
        removes a distributions entry points from the storage
        """
        if distname in self.get_dist_names():
            self.epmap.pop(distname)

    def get_map(self, dist=None, group=None, name=None):
        """
        see BackendInterface docs
        """
        import re
        from collections import Sequence
        from sparkplug.entrypoint import EntryPoint
        '''sanitize dist kwarg'''
        if dist is None:
            dist = self.get_dist_names()
        if not isinstance(dist, Sequence) or isinstance(dist, str):
            dist = [dist]

        '''sanitize groups kwarg'''
        if group is None:
            group = self.get_group_names()
        if not isinstance(group, Sequence) or isinstance(group, str):
            group = [group]

        '''sanitize name kwarg'''
        if name is not None:
            if not isinstance(name, Sequence) or isinstance(name, str):
                name = [name]

        emap = {}
        for d in dist:
            emap[d] = {}
            for g in group:
                if g in self.epmap.get(d, {}):
                    gmap = self.epmap.get(d, {}).get(g, {})
                    emap[d][g] = {}
                    for n, e in gmap.iteritems():
                        if not name or any([re.match(i, n) for i in name]):
                            emap[d][g][n] = EntryPoint.parse(e)
        return emap

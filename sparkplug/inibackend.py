# -*- coding: utf8 -*-
from ConfigParser import SafeConfigParser

from sparkplug.abcbackend import BackendInterface


class IniBackend(object):
    """
    Backend using the standard python configparser
    """
    def __init__(self):
        super(IniBackend, self).__init__()
        self.eppars = SafeConfigParser()
        self.dstpars = SafeConfigParser()
        from os.path import join, dirname, exists
        self.datafile = join(dirname(__file__), 'ini_data')
        self.distfile = join(dirname(__file__), 'ini_dist')
        if not exists(self.datafile):
            with open(self.datafile, 'w') as data:
                data.write('')
        if not exists(self.distfile):
            with open(self.distfile, 'w') as dist:
                dist.write('[pkgmap]')
        self.eppars.read(self.datafile)
        self.dstpars.read(self.distfile)

    def write_dist(self, dist):
        """
        add a distribution, empty by default
        """
        from os.path import exists
        from pkg_resources import get_distribution

        dist = get_distribution(dist)
        dname = dist.project_name

        '''write or edit the section for the distribution'''
        if not self.dstpars.has_section(dname):
            self.dstpars.add_section(dname)

        '''write entry points and package-dist'''
        epmap = dist.get_entry_map()
        pkgset = set()
        for group, eps in epmap.iteritems():
            '''open a section for the group if necessary
            add an option for each entry point'''
            if not self.eppars.has_section(group):
                self.eppars.add_section(group)
            for name, ep in eps.iteritems():
                pkgset.add(ep.module_name.split('.', 1)[0])
                val = '{}:{}'.format(ep.module_name, '.'.join(ep.attrs))
                '''this will overwrite clashing entry points'''
                self.eppars.set(group, name, val)
                self.dstpars.set(dname, name, group)

        '''keep a list of which package belongs to which dist'''
        for pkg in pkgset:
            self.dstpars.set('pkgmap', pkg, dname)

        '''write to files'''
        with open(self.datafile, 'w') as datafile:
            self.eppars.write(datafile)
        with open(self.distfile, 'w') as distfp:
            self.dstpars.write(distfp)

    def mkspec(self, item):
        return '{i[0]} = {i[1]}'.format(i=item)

    def iter_group(self, group):
        """
        returns a list of entry points for the given group name
        """
        from sparkplug.entrypoint import EntryPoint

        return (EntryPoint.parse(self.mkspec(i)) for i in self.eppars.items(group))

    def get_dist_map(self, dist):
        """
        returns a n entry map for a given dist (or package) name
        """
        if self.dstpars.has_section(dist):
            dname = dist
        elif self.dstpars.has_option('pkgmap', dist):
            dname = self.dstpars.get('pkgmap', dist)
        else:
            return {}

        from sparkplug.entrypoint import EntryPoint
        eplist = self.dstpars.items(dname)
        groups = set([k[1] for k in eplist])
        epmap = {i: [] for i in groups}
        for ep, group in eplist:
            lhs = self.eppars.get(group, ep)
            spc = self.mkspec((ep, lhs))
            epmap[group].append(EntryPoint.parse(spc))

        return epmap

    def get_ep(self, group, name, dist=None):
        """
        returns an entry point.
        """
        from sparkplug.entrypoint import EntryPoint
        lhs = self.eppars.get(group, name)
        ep = EntryPoint.parse(self.mkspec(self

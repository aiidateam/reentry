# -*- coding: utf8 -*-
from ConfigParser import SafeConfigParser

from sparkplug.abcbackend import BackendInterface


class IniBackend(object):
    """
    Backend using the standard python configparser
    """
    def __init__(self):
        super(IniBackend, self).__init__()
        self.cfgpars = SafeConfigParser()
        from os.path import join, dirname, exists
        self.datafile = join(dirname(__file__), 'ini_data')
        if not exists(self.datafile):
            with open(self.datafile, 'w') as data:
                data.write('')
        self.cfgpars.read(self.datafile)

    def distfile(self, distname):
        from os.path import join, dirname, exists
        datafile = join(dirname(__file__), distname)
        if not exists(datafile):
            with open(datafile, 'w'):
                datafile.write('')

    def write_dist(self, dist):
        """
        add a distribution, empty by default
        """
        from os.path import exists
        from pkg_resources import get_distribution

        dist = get_distribution(dist)
        epmap = dist.get_entry_map()
        for group, eps in epmap.iteritems():
            if not self.cfgpars.has_section(group):
                self.cfgpars.add_section(group)
            for name, ep in eps.iteritems():
                val = '{}:{}'.format(ep.module_name, '.'.join(ep.attrs))
                self.cfgpars.set(group, name, val)
        with open(self.datafile, 'w') as datafile:
            self.cfgpars.write(datafile)

    def mkspec(self, item):
        return '{i[0]} = {i[1]}'.format(i=item)

    def get_group(self, group):
        """
        returns a list of entry points for the given group name
        """
        from sparkplug.entrypoint import EntryPoint

        return [EntryPoint.parse(self.mkspec(i)) for i in self.cfgpars.items(group)]

# -*- coding: utf8 -*-
"""Light weight entry point implementation"""
import re


class EntryPoint(object):
    """
    Lightweight analogue for pkg_resources.EntryPoint
    """
    pattern = re.compile(r'\s*(?P<name>.+?)\s*=\s*(?P<module>[\w.]+)\s*(:\s*(?P<attr>[\w.]+))?\s*(?P<extras>\[.*\])?\s*$')

    def __init__(self, name, module_name, attrs=(), distname=None):
        self.name = name
        self.module_name = module_name
        self.attrs = attrs
        self.distname = distname

    @classmethod
    def parse(cls, src, distname=None):
        """
        pasted from pkg_resources, fall back on their EntryPoints when extras are required
        """
        match = cls.pattern.match(src)
        res = match.groupdict()
        if res['extras']:
            import pkg_resources as pr
            dist = pr.get_distribution(distname) if distname else None
            return pr.EntryPoint.parse(src, dist=dist)
        attrs = res['attr'].split('.') if res['attr'] else ()
        return cls(res['name'], res['module'], attrs, distname)

    def load(self):
        """
        pasted from pkg_resources
        """
        import functools
        from importlib import import_module
        module = import_module(self.module_name)
        try:
            return functools.reduce(getattr, self.attrs, module)
        except AttributeError as exc:
            raise ImportError(str(exc))

    def __str__(self):
        string_form = '{} = {}'.format(self.name, self.module_name)
        if self.attrs:
            string_form += ':{}'.format('.'.join(self.attrs))
        return string_form

    def __repr__(self):
        return 'reentry.EntryPoint.parse({})'.format(str(self))

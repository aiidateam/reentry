# -*- coding: utf8 -*-
from reentry.jsonbackend import JsonBackend


bkend = JsonBackend()


def iter_entry_points(group, name=None):
    """
    returns all registered entry points in `group`, or if `name` is given,
    only the ones matching `name`.

    The backend may only load pkg_resources if any of the entry points contain extras requirements
    """
    for ep in bkend.iter_group(group):
        if name:
            if name in ep.name:
                yield ep
        else:
            yield ep


def get_entry_map(distname, group=None):
    """
    return the entry point map for `group` or the whole map for `dist`

    The backend may only load pkg_resources if any of the entry points contain extras requirements
    """
    return bkend.get_map(dist=distname, group=group)


def register(distname):
    """
    registers the distribution's entry points with the backend

    The backend may load pkg_resources to resolve the distribution name
    """
    bkend.write_dist(distname)


def scan(groups=[], group_re=None):
    """
    walks through all distributions available and registers entry points or only those in `groups`
    """
    import pkgutil
    import sys
    import pkg_resources as pr
    pr_env = pr.AvailableDistributions()
    pr_env.scan()
    if groups:
        for g in groups:
            bkend.rm_group(g)
    else:
        bkend.clear()

    for dists in pr_env._distmap.values():
        dist = dists[0]
        emap = dist.get_entry_map()
        if groups:
            dmap = {k: v for k, v in emap.iteritems() if k in groups}
        elif group_re:
            dmap = {k: v for k, v in emap.iteritems() if group_re.match(k)}
        else:
            dmap = emap
        dname = dist.project_name
        bkend._write_dist(dname, dmap)


def unregister(distname):
    """
    unregisters the distribution's entry points with the backend

    The backend may load pkg_resources to resolve the distribution name
    """
    bkend.rm_dist(distname)

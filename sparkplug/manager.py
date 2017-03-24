# -*- coding: utf8 -*-
from sparkplug.jsonbackend import JsonBackend


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


def register_all(groups=[]):
    """
    walks through all distributions available and registers entry points or only those in `groups`
    """
    import pkgutil
    import sys
    import pkg_resources as pr
    from mdebug.mdebug import mdebug
    DBG = mdebug()
    pr_env = pr.AvailableDistributions()
    pr_env.scan()
    # ~ modules = (i[1] for i in pkgutil.iter_modules() if i[2] and i[1].find('.') < 0)
    # ~ modules = [mod for mod in modules if mod not in sys.builtin_module_names]
    # ~ modules = [mod for mod in modules if not mod.startswith('_')]
    for dists in pr_env._distmap.values():
        dist = dists[0]
        DBG(dist)
        # ~ try:
            # ~ DBG(mod)
            # ~ dist = DBG(pr.get_distribution(mod))
        # ~ except pr.DistributionNotFound as e:
            # ~ DBG(e)
            # ~ continue
        emap = DBG(dist.get_entry_map())
        if groups:
            emap = {k: v for k, v in emap.iteritems() if k in groups}
        dname = dist.project_name
        bkend._write_dist(DBG(dname), DBG(emap))
        print('---')


def unregister(distname):
    """
    unregisters the distribution's entry points with the backend

    The backend may load pkg_resources to resolve the distribution name
    """
    bkend.rm_dist(distname)

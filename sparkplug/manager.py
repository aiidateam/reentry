# -*- coding: utf8 -*-
from sparkplug.jsonbackend import JsonBackend


bkend = JsonBackend()


def iter_entry_points(group, name=None):
    """
    returns all registered entry points in `group`, or if `name` is given,
    only the ones matching `name`.
    """
    for ep in bkend.iter_group(group):
        if name:
            if name in ep.name:
                yield ep
        else:
            yield ep

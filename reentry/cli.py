import click


@click.group()
def reentry():
    """manage your reentry python entry point cache"""


@reentry.command()
@click.argument('groups', nargs=-1, metavar='PATTERN')
@click.option('-r', '--regex', is_flag=True, help='Treat PATTERNs as regular expresions')
def scan(groups, regex):
    """
    Scan for python entry points to cache for faster loading.

    Scan only for specific PATTERNs or leave empty to scan all
    """
    from reentry.manager import scan as scan_groups
    from reentry.manager import bkend

    if regex:
        if not groups:
            '''nothing to do'''
            click.exit()
        import re
        matchstr = re.compile("|".join(['({})'.format(i) for i in groups]))
        scan_groups(group_re=matchstr)
    else:
        scan_groups(groups)


@reentry.command()
@click.option('--dist', help='limit map to a distribution')
@click.option('--group', help='limit map to an entry point group')
@click.option('--name', help='limit map to entrypoints that match NAME')
def map(dist, group, name):
    import pprint
    from reentry.manager import bkend
    if dist is None:
        res = {d: bkend.get_map(d, group, name) for d in bkend.get_dist_names()}
    else:
        res = bkend.get_map(dist, group, name)
    click.echo(pprint.pformat(res))

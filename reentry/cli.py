"""Command line interface for reentry"""
import sys
import os
import subprocess

import click

from reentry.config import get_datafile


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
    from reentry import manager

    if regex:
        if not groups:
            # nothing to do
            sys.exit(0)
        import re
        matchstr = re.compile("|".join(['({})'.format(i) for i in groups]))
        manager.scan(group_re=matchstr)
    else:
        manager.scan(groups)


@reentry.command('map')
@click.option('--dist', help='limit map to a distribution')
@click.option('--group', help='limit map to an entry point group')
@click.option('--name', help='limit map to entrypoints that match NAME')
def map_(dist, group, name):
    """Print out a map of cached entry points"""
    import pprint
    from reentry import manager
    if dist is None:
        res = {d: manager.get_entry_map(d, group, name) for d in manager.distribution_names}
    else:
        res = manager.get_entry_map(dist, group, name)
    click.echo(pprint.pformat(res))


@reentry.group('dev')
def dev():
    """Development related commands."""


def echo_call(cmd):
    click.echo('calling: {}'.format(' '.join(cmd)), err=True)


@dev.command()
def coveralls():
    """Run coveralls only on travis."""
    if os.getenv('TRAVIS'):
        cmd = ['coveralls']
        echo_call(cmd)
        subprocess.call(cmd)


@dev.command('datafile')
def datafile():
    """Print the path to the current datafile."""
    click.echo(get_datafile())

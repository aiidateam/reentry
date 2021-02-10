"""CLI for reentry integration test.

Note: This requires the test packages in .github/ to be installed first.
"""
from __future__ import print_function

import click

try:
    # prefer the backport for Python <3.5
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

from reentry import manager
from reentry.config import get_datafile


@click.command()
@click.option('--with-noreg', is_flag=True)
def main(with_noreg):
    """Test automatic scanning / registering"""
    entry_point_map = manager.get_entry_map(groups='reentry_test', ep_names=['test-plugin', 'test-noreg', 'builtin'])
    data_file = Path(get_datafile())

    assert entry_point_map, 'The \'reentry_test\' entry point group was not found\nMap:\n{}\n\nData File: {}\n\nContents:\n{}'.format(
        manager.get_entry_map(), str(data_file), data_file.read_text())

    try:
        test_entry_point = entry_point_map['reentry_test']['test-plugin']
        builtin_entry_point = entry_point_map['reentry_test']['builtin']
        if with_noreg:
            # note: `reentry scan` for this work
            noreg_entry_point = entry_point_map['reentry_test']['test-noreg']
    except Exception as err:
        print('datafile: {}'.format(str(data_file)))
        print('\nCurrent relevant entry point map:\n\n')
        print(manager.format_map(entry_point_map))
        print('\n')
        scan_map = manager.scan(groups=['reentry_test'], commit=False)
        print('\nFull entry point map after scan:\n\n')
        print(manager.format_map(scan_map))
        raise err

    plugin_class = test_entry_point.load()
    builtin_class = builtin_entry_point.load()

    assert plugin_class.test_string == 'TEST', 'The test string was incorrect'
    assert builtin_class.test_string == 'TEST', 'The test string was incorrect'
    if with_noreg:
        noreg_class = noreg_entry_point.load()
        assert noreg_class.test_string == 'TEST', 'The test string was incorrect'

    plugin_list = [ep.load() for ep in manager.iter_entry_points('reentry_test')]
    assert plugin_class in plugin_list, 'iter_entry_points found differing test entry point from get_entry_map.'
    assert builtin_class in plugin_list, 'iter_entry_points found differing test entry point from get_entry_map.'
    if with_noreg:
        assert noreg_class in plugin_list, 'iter_entry_points found differing test entry point from get_entry_map.'

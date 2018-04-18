"""Test main for integration test, requires the test plugin to be installed first."""
from __future__ import print_function
from py import path as py_path  # pylint: disable=no-name-in-module

from reentry import manager
from reentry.config import get_datafile


def main():
    """Test automatic scanning / registering"""
    entry_point_map = manager.get_entry_map(groups='reentry_test', ep_names=['test-plugin', 'test-noreg'])
    data_file = py_path.local(get_datafile())

    assert entry_point_map, 'The test plugin entry point were not found\nMap:\n{}\n\nData File: {}\n\nContents:\n{}'.format(
        manager.get_entry_map(), data_file.strpath, data_file.read())

    try:
        test_entry_point = entry_point_map['reentry_test']['test-plugin']
        noreg_entry_point = entry_point_map['reentry_test']['test-noreg']
        builtin_entry_point = entry_point_map['reentry_test']['builtin']
    except Exception as err:
        scan_map = manager.scan(groups=['reentry_test'], nocommit=True)
        print('\n'.join(['{} -> {}'.format(dname, dmap) for dname, dmap in scan_map.items()]))
        print(entry_point_map)
        raise err

    plugin_class = test_entry_point.load()
    noreg_class = noreg_entry_point.load()
    builtin_class = builtin_entry_point.load()

    assert plugin_class.test_string == 'TEST', 'The test string was incorrect'
    assert noreg_class.test_string == 'TEST', 'The test string was incorrect'
    assert builtin_class.test_string == 'TEST', 'The test string was incorrect'

    plugin_list = [ep.load() for ep in manager.iter_entry_points('reentry_test')]
    assert plugin_class in plugin_list, 'iter_entry_points found differing test entry point from get_entry_map.'
    assert noreg_class in plugin_list, 'iter_entry_points found differing test entry point from get_entry_map.'
    assert builtin_class in plugin_list, 'iter_entry_points found differing test entry point from get_entry_map.'

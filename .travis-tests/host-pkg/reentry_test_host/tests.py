"""Test main for integration test, requires the test plugin to be installed first."""
from py import path as py_path  # pylint: disable=no-name-in-module

from reentry import manager
from reentry.config import get_datafile


def main():
    """Test automatic scanning / registering"""
    entry_point_map = manager.get_entry_map(dist_names='reentry-test-plugin', groups='reentry_test', ep_names='test-plugin')
    data_file = py_path.local(get_datafile())

    assert entry_point_map, 'The test plugin entry point was not found\nMap:\n{}\n\nData File: {}\n\nContents:\n{}'.format(
        manager.get_entry_map(), data_file.strpath, data_file.read())
    test_entry_point = entry_point_map['reentry_test']['test-plugin']

    plugin_class = test_entry_point.load()

    assert plugin_class.test_string == 'TEST', 'The test string was incorrect'

    assert list(manager.iter_entry_points('reentry_test'))[
        0].load() == plugin_class, 'iter_entry_points found differing test entry point from get_entry_map.'

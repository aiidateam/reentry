"""Test main for integration test, requires the test plugin to be installed first."""
from py import path as py_path  # pylint: disable=no-name-in-module

from reentry import manager
from reentry.config import get_datafile

if __name__ == '__main__':
    ENTRY_POINT_MAP = manager.get_entry_map(dist_names='reentry-test-plugin', groups='reentry_test', ep_names='test-plugin')
    DATA_FILE = py_path.local(get_datafile())

    assert ENTRY_POINT_MAP, 'The test plugin entry point was not found\nMap:\n{}\n\nData File: {}\n\nContents:\n{}'.format(
        manager.get_entry_map(), DATA_FILE.strpath, DATA_FILE.read())
    TEST_EP = ENTRY_POINT_MAP['reentry_test']['test-plugin']

    PLUGIN_CLASS = TEST_EP.load()

    assert PLUGIN_CLASS.test_string == 'TEST', 'The test string was incorrect'

    assert list(manager.iter_entry_points('reentry_test'))[
        0].load() == PLUGIN_CLASS, 'iter_entry_points found differing test entry point from get_entry_map.'

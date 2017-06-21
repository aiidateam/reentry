"""Unit tests for manager functions"""
import pytest


@pytest.fixture
def bkend():
    """create a backend with test data"""
    from os.path import join, dirname
    from ..jsonbackend import JsonBackend
    test_file = join(dirname(__file__), 'test_data.json')
    return JsonBackend(datafile=test_file)


def test_get_entry_map(bkend):
    """
    The map for distA in the fixture should contain
    a group and an entry point
    """
    from .. import manager
    manager.bkend = bkend
    epmap = manager.get_entry_map('distA')
    assert 'groupA' in epmap
    assert 'distA.epA' in epmap.get('groupA', {})

# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for manager functions"""
import re
import pytest

from fixtures import test_data, bkend, manager, noscan_manager


def test_get_entry_map(manager):
    """test full map"""
    epmap = manager.get_entry_map()
    assert 'groupA' in epmap
    assert 'groupB' in epmap
    assert 'groupC' in epmap


def test_get_entry_map_dist(manager):
    """
    The map for distA in the fixture should contain
    a group and an entry point
    """
    epmap = manager.get_entry_map(dist_names='distA')
    assert 'groupA' in epmap
    assert 'groupB' in epmap
    assert 'groupC' not in epmap
    assert 'distA.epA' in epmap.get('groupA', {})
    assert 'distA.epB' in epmap.get('groupB', {})


def test_entry_map_dist_group(manager):
    """Check filtering entry point map for a distribution by group"""
    epmap = manager.get_entry_map(dist_names='distA', groups='groupA')
    assert 'groupA' in epmap
    assert 'groupB' not in epmap
    assert 'distA.epA' in epmap.get('groupA', {})


def test_iter_entry_points(manager):
    """Test the drop-in replacement for pkg_resources.iter_entry_points"""
    entry_points = manager.iter_entry_points(group='groupA')
    assert 'distA.epA' in [e.name for e in entry_points]

    entry_points = list(manager.iter_entry_points(group='groupB'))
    assert 'distA.epB' in [e.name for e in entry_points]
    assert 'distB.epB' in [e.name for e in entry_points]


def test_register(manager):
    """Test registering a distribution"""
    manager.register('reentry')
    ep_map = manager.get_entry_map(dist_names='reentry')
    assert 'test_entry_points' in ep_map
    assert 'console_scripts' not in ep_map


def test_scan(manager):
    """Test scanning for entry points"""
    manager.scan()
    ep_map = manager.get_entry_map(dist_names='reentry')
    assert 'test_entry_points' in ep_map
    assert 'console_scripts' not in ep_map


def test_scan_group(manager):
    manager.scan(groups=['test_entry_points'])
    ep_map = manager.get_entry_map(dist_names='reentry')
    assert 'test_entry_points' in ep_map
    assert 'console_scripts' not in ep_map


def test_scan_group_re(manager):
    manager.scan(group_re=re.compile(r'test_[a-z]+_[a-z]+'))
    assert 'test_entry_points' in manager.get_entry_map(dist_names='reentry')
    manager.scan(group_re=r'console.*')
    assert 'console_scripts' in manager.get_entry_map(dist_names='reentry')


def test_unregister(manager):
    manager.unregister('distA')
    assert 'distA' not in manager.distribution_names


def test_iter_scan(manager):
    assert 'test' in [ep.name for ep in manager.iter_entry_points(group='test_entry_points')]
    assert 'reentry' in [ep.name for ep in manager.iter_entry_points(group='console_scripts', name='reentry')]


def test_iter_noscan(noscan_manager):
    assert 'test' not in [ep.name for ep in noscan_manager.iter_entry_points(group='test_entry_points')]

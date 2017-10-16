# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for manager functions"""
import pytest

from reentry.tests.fixtures import test_data, bkend, manager


def test_get_entry_map(manager):
    """
    The map for distA in the fixture should contain
    a group and an entry point
    """
    epmap = manager.get_entry_map('distA')
    assert 'groupA' in epmap
    assert 'groupB' in epmap
    assert 'groupC' not in epmap
    assert 'distA.epA' in epmap.get('groupA', {})
    assert 'distA.epB' in epmap.get('groupB', {})


def test_entry_map_group(manager):
    """Check filtering entry point map for a distribution by group"""
    epmap = manager.get_entry_map('distA', group='groupA')
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

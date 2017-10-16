# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for manager functions"""
import pytest

from reentry.tests.fixtures import bkend, manager


def test_get_entry_map(manager):
    """
    The map for distA in the fixture should contain
    a group and an entry point
    """
    epmap = manager.get_entry_map('distA')
    assert 'groupA' in epmap
    assert 'distA.epA' in epmap.get('groupA', {})


def test_entry_map_group(manager):
    epmap = manager.get_entry_map('distA', group='groupA')
    assert 'distA.epA' in epmap.get('groupA', {})

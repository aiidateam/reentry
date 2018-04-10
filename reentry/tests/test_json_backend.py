# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for js-backend"""
import json

import pytest

from reentry.tests.fixtures import test_data, bkend
from reentry.entrypoint import EntryPoint


def test_get_map_default(bkend):
    """Test the backend's get_map method without arguments"""
    ep_map = bkend.get_map()

    assert 'groupB' in ep_map
    assert 'distA.epB' in ep_map['groupB']
    assert 'distB.epB' in ep_map['groupB']
    assert isinstance(ep_map['groupB']['distB.epB'], EntryPoint)


def test_get_map_by_dist(bkend):
    """Test get_map output filtering with dist"""
    ep_map = bkend.get_map(dist='distA')
    assert 'distA.epB' in ep_map['groupB']
    assert 'distB.epB' not in ep_map['groupB']

    ep_map = bkend.get_map(dist=['distA', 'distB'])
    assert 'distA.epB' in ep_map['groupB']
    assert 'distB.epB' in ep_map['groupB']


def test_get_map_by_group(bkend):
    """Test get_map output filtering with group"""
    ep_map = bkend.get_map(group='groupA')
    assert 'groupA' in ep_map
    assert 'groupB' not in ep_map

    ep_map = bkend.get_map(group=['groupA', 'groupB'])
    assert 'groupA' in ep_map
    assert 'groupB' in ep_map
    assert 'groupC' not in ep_map


def test_get_map_by_name(bkend):
    """Test get_map ouptut filering with name"""
    ep_map = bkend.get_map(name=r'.*\.epB')
    assert 'distA.epB' in ep_map['groupB']
    assert 'distB.epB' in ep_map['groupB']
    assert 'groupA' not in ep_map

    ep_map = bkend.get_map(name=[r'.*\.epB', 'distB.epC'])
    assert 'distA.epB' in ep_map['groupB']
    assert 'distB.epC' in ep_map['groupC']
    assert 'groupA' not in ep_map


def test_iter_group(bkend):
    ep_list = list(bkend.iter_group('groupB'))
    assert 'distA.epB' in [i.name for i in ep_list]
    assert 'distB.epB' in [i.name for i in ep_list]


def test_group_names(bkend):
    group_names = bkend.get_group_names()
    assert 'groupA' in group_names
    assert 'groupB' in group_names
    assert 'groupC' in group_names


def test_dist_names(bkend):
    dist_names = bkend.get_dist_names()
    assert 'distA' in dist_names
    assert 'distB' in dist_names


def test_write_dist_map(bkend):
    entry_point_map = {'test_group': {'test_ep': 'test_ep = test_dist.test_module:test_member'}}
    bkend.write_dist_map(distname='test_dist', entry_point_map=entry_point_map)
    assert 'test_dist' in list(bkend.get_dist_names())
    assert bkend.get_map(dist='test_dist')


def test_write_pr_dist(bkend):
    """Test caching entry points for a given pkg_resources - distribution"""
    this_dist = bkend.pr_dist_from_name('reentry')
    bkend.write_pr_dist(this_dist)
    assert 'reentry' in list(bkend.get_dist_names())
    assert bkend.get_map(dist='reentry')


def test_write_st_dist(bkend):
    """Test caching entry points for a distribution given by name."""
    bkend.write_st_dist('reentry')
    assert 'reentry' in list(bkend.get_dist_names())
    assert bkend.get_map(dist='reentry')


def test_write_install_dist(bkend):
    """Test caching entry points for a pkg_resources - distribution at install time."""
    this_dist = bkend.pr_dist_from_name('reentry')
    this_dist.get_name = lambda: 'reentry'
    this_dist.entry_points = {'foo': ['bar = foo.bar:baz']}
    bkend.write_install_dist(this_dist)
    assert 'reentry' in list(bkend.get_dist_names())
    assert 'foo' in bkend.get_map(dist='reentry')


def test_rm_dist(bkend):
    bkend.rm_dist('distA')
    assert 'distA' not in bkend.epmap


def test_clear(bkend):
    bkend.clear()
    assert not bkend.get_map()

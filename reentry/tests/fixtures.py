# pylint: disable=unused-import,redefined-outer-name
"""Unit test fixtures"""
import pytest


@pytest.fixture
def bkend():
    """create a backend with test data"""
    from os.path import join, dirname
    from ..jsonbackend import JsonBackend
    test_file = join(dirname(__file__), 'test_data.json')
    return JsonBackend(datafile=test_file)


@pytest.fixture
def manager(bkend):
    from reentry.manager import PluginManager
    manager = PluginManager(backend=bkend)
    yield manager

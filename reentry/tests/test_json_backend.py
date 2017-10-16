# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for js-backend"""
import json

import pytest

from reentry.tests.fixtures import test_data, bkend
from reentry.entrypoint import EntryPoint


def test_get_map(bkend):
    ep_map = bkend.get_map()

    assert 'groupB' in ep_map
    assert 'distA.epB' in ep_map['groupB']
    assert 'distB.epB' in ep_map['groupB']
    assert isinstance(EntryPoint, ep_map['groupB']['distB.epB'])

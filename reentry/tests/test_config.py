# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for config tools."""
try:
    # prefer the backport for Python <3.5
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

import pytest  # pylint: disable=unused-import
import os
import six
from six.moves import configparser

from reentry import config


def test_find_config():
    config_file = config.find_config()
    assert isinstance(config_file, Path)


def test_make_config_parser():
    """Make sure we get the right configparser type."""
    parser = config.make_config_parser()
    if six.PY2:
        assert isinstance(parser, configparser.SafeConfigParser)
    else:
        assert isinstance(parser, configparser.ConfigParser)

def _check_config_valid(parser, expected_filename=None):
    if six.PY2:
        assert isinstance(parser, configparser.SafeConfigParser)
    else:
        assert isinstance(parser, configparser.ConfigParser)

    assert parser.get('general', 'datadir')
    assert parser.get('general', 'data_filename')
    if expected_filename:
        assert parser.get('general', 'data_filename') == expected_filename

def test_get_config():
    """Make sure the configparser gets created correctly."""
    parser = config.get_config()
    _check_config_valid(parser)


def test_get_config_with_data_filename():
    """Make sure the configparser gets created correctly when REENTRY_DATA_FILENAME is set."""
    data_filename = 'entrypoints'
    os.environ['REENTRY_DATA_FILENAME'] = data_filename
    parser = config.get_config()
    os.environ.pop('REENTRY_DATA_FILENAME')

    _check_config_valid(parser, data_filename)


def test_get_datafile():
    datafile = Path(config.get_datafile())

    assert datafile.is_file()
    assert datafile.exists()

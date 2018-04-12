# pylint: disable=unused-import,redefined-outer-name
"""Unit tests for config tools."""
import pytest  # pylint: disable=unused-import
from py import path as py_path  # pylint: disable=no-name-in-module
import six
from six.moves import configparser

from reentry import config


def test_find_config():
    config_file = config.find_config()
    assert isinstance(config_file, py_path.local)


def test_make_config_parser():
    """Make sure we get the right configparser type."""
    parser = config.make_config_parser()
    if six.PY2:
        assert isinstance(parser, configparser.SafeConfigParser)
    else:
        assert isinstance(parser, configparser.ConfigParser)


def test_get_config():
    """Make sure the configparser gets created correctly."""
    parser = config.get_config()

    if six.PY2:
        assert isinstance(parser, configparser.SafeConfigParser)
    else:
        assert isinstance(parser, configparser.ConfigParser)

    assert parser.get('general', 'datadir')


def test_get_datafile():
    datafile = py_path.local(config.get_datafile())

    assert datafile.isfile()
    assert datafile.exists()

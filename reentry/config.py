"""Find and read user settings."""
import os

import six
from six.moves import configparser
from py import path as py_path  # pylint: disable=no-name-in-module

__all__ = ['find_config', 'get_config', 'get_datafile']


def find_config():
    """
    Search for a config file in the following places and order:

        * <HOME>/.reentryrc
        * <HOME>/.config/reentry/config
    """
    home = py_path.local(os.path.expanduser('~'))
    rc_file = home.join('.reentryrc')
    config_file = home.join('.config', 'reentry', 'config')
    if home.exists():
        return rc_file
    elif config_file.exists():
        return config_file
    return rc_file


def make_config_parser(*args, **kwargs):
    """Get the correct ConfigParser class depending on python version."""
    if six.PY2:
        return configparser.SafeConfigParser(*args, **kwargs)
    elif six.PY3:
        return configparser.ConfigParser(*args, **kwargs)
    return None


def get_config(config_file_name=find_config().strpath):
    """Create config parser with defaults and read in the config file."""
    default_config_dir = py_path.local(os.path.expanduser('~/.config/reentry'))
    parser = make_config_parser({'datadir': default_config_dir.join('data').strpath})
    parser.add_section('general')
    parser.read([config_file_name])
    return parser


def get_datafile():
    """Create the path to the data file used to store entry points."""
    config = get_config()
    sep = os.path.sep
    pkg_path_filename = py_path.local(__file__).dirname.lstrip(sep).replace(sep, '.')
    datafile = py_path.local(config.get('general', 'datadir')).join(pkg_path_filename)
    datafile.ensure()
    if not datafile.read():
        datafile.write('{}')
    return datafile.strpath

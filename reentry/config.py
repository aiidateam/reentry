"""Find and read user settings."""
import os
from configparser import ConfigParser

from py import path as py_path  # pylint: disable=no-name-in-module
from reentry import __path__ as reentry_path


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


def get_config(config_file_name=find_config()):
    """Create config parser with defaults and read in the config file."""
    default_config_dir = py_path.local(os.path.expanduser('~/.config/reentry'))
    parser = ConfigParser({'datadir': default_config_dir.join('data').strpath}, default_section='general')
    parser.read([config_file_name.strpath])
    return parser


def get_datafile():
    """Create the path to the data file used to store entry points."""
    config = get_config()
    sep = os.path.sep
    pkg_path_filename = py_path.local(reentry_path[0]).strpath.lstrip(sep).replace(sep, '.')
    datafile = py_path.local(config.get('general', 'datadir')).join(pkg_path_filename)
    datafile.ensure()
    if not datafile.read():
        datafile.write('{}')
    return datafile.strpath

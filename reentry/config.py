"""Find and read user settings."""
import os
import sys
import hashlib
import platform
try:
    # prefer the backport for Python <3.5
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

import six
from six.moves import configparser

__all__ = ['find_config', 'get_config', 'get_datafile']


def _get_default_config_dir():
    return Path(os.getenv('XDG_CONFIG_HOME', '~/.config')).expanduser().joinpath('reentry')


def find_config():
    """
    Search for a config file in the following places and order:

        * <HOME>/.reentryrc
        * <HOME>/.config/reentry/config
    """
    rc_file = Path.home().joinpath('.reentryrc')
    config_file = _get_default_config_dir().joinpath('config')
    # pylint: disable=no-else-return
    if rc_file.exists():  # pylint: disable=no-member
        return rc_file
    elif config_file.exists():  # pylint: disable=no-member
        return config_file
    return rc_file


def make_config_parser(*args, **kwargs):
    """Get the correct ConfigParser class depending on python version."""
    # pylint: disable=no-else-return
    if six.PY2:
        return configparser.SafeConfigParser(*args, **kwargs)
    elif six.PY3:
        return configparser.ConfigParser(*args, **kwargs)
    return None


def get_config(config_file_name=str(find_config())):
    """Create config parser with defaults and read in the config file."""
    default_config_dir = _get_default_config_dir()
    default_config_values = {'datadir': str(default_config_dir.joinpath('data')), 'data_filename': hashed_data_file_name()}
    parser = make_config_parser(default_config_values)
    parser.add_section('general')
    parser.read([config_file_name])

    env_datadir = os.getenv('REENTRY_DATADIR')
    if env_datadir:
        env_datadir_path = Path(env_datadir)
        if env_datadir_path.exists() and not env_datadir_path.is_dir():  # pylint: disable=no-member
            raise ValueError('environment variable $REENTRY_DATADIR={} exists, but is not a directory'.format(env_datadir))
        parser.set('general', 'datadir', str(env_datadir_path))

    env_data_filename = os.getenv('REENTRY_DATA_FILENAME')
    if env_data_filename:
        parser.set('general', 'data_filename', env_data_filename)

    return parser


def hashed_data_file_name():
    """Find the path to the reentry executable and mangle it into a file name."""

    fname = 'u{bin_dir}_{impl}-{ver}'.format(bin_dir=Path(sys.executable).resolve().parent,
                                             impl=platform.python_implementation(),
                                             ver=platform.python_version())

    path_hash = hashlib.sha256(fname.encode('utf-8'))
    return path_hash.hexdigest()


def get_datafile():
    """Create the path to the data file used to store entry points."""
    config = get_config()

    pkg_path_filename = config.get('general', 'data_filename')
    datafile = Path(config.get('general', 'datadir')).joinpath(pkg_path_filename)
    if not datafile.exists():  # pylint: disable=no-member
        datafile.parent.mkdir(parents=True, exist_ok=True)
        datafile.write_text(u'{}')

    return str(datafile)

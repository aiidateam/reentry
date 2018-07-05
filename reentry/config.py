"""Find and read user settings."""
import os
import sys
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
    if rc_file.exists():  # pylint: disable=no-member
        return rc_file
    elif config_file.exists():  # pylint: disable=no-member
        return config_file
    return rc_file


def make_config_parser(*args, **kwargs):
    """Get the correct ConfigParser class depending on python version."""
    if six.PY2:
        return configparser.SafeConfigParser(*args, **kwargs)
    elif six.PY3:
        return configparser.ConfigParser(*args, **kwargs)
    return None


def get_config(config_file_name=str(find_config())):
    """Create config parser with defaults and read in the config file."""
    default_config_dir = _get_default_config_dir()
    parser = make_config_parser({'datadir': str(default_config_dir.joinpath('data'))})
    parser.add_section('general')
    parser.read([config_file_name])

    env_datadir = os.getenv('REENTRY_DATADIR')
    if env_datadir:
        env_datadir_path = Path(env_datadir)
        if env_datadir_path.exists() and not env_datadir_path.is_dir():  # pylint: disable=no-member
            raise ValueError('environment variable $REENTRY_DATADIR={} exists, but is not a directory'.format(env_datadir))
        parser.set('general', 'datadir', str(env_datadir_path))

    return parser


def make_data_file_name():
    """Find the path to the reentry executable and mangle it into a file name."""
    sep = os.path.sep
    python_bin_dir = str(Path(sys.executable).parent)
    py_version = 'UNKNOWN'
    if six.PY2:
        py_version = 'PY2'
    elif six.PY3:
        py_version = 'PY3'
    file_name = python_bin_dir.lstrip(sep).replace(sep, '.').replace('.', '_') + '_' + py_version
    return file_name


def get_datafile():
    """Create the path to the data file used to store entry points."""
    config = get_config()
    pkg_path_filename = make_data_file_name()
    datafile = Path(config.get('general', 'datadir')).joinpath(pkg_path_filename)

    if not datafile.exists():  # pylint: disable=no-member
        datafile.parent.mkdir(parents=True, exist_ok=True)
        datafile.write_text(u'{}')

    return str(datafile)

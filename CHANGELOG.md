# Changelog
All notable changes to this project after version 1.0.3 will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2019-04-10

### Changed
 - drop support for `reentry_scan` hook since pip 19 introduced build-system isolation that restricts 
   scans performed by the hook to the build-system (containing only setuptools, wheel, reentry, etc.).
 - `manager.scan`: renamed negated options (`nocommit` => `commit`, `nodelete` => `delete`)

### Added
 - add `reentry clear` command to clear the reentry cache

## [1.2.2] - 2018-10-07

### Changed
 - replace py with pathlib/pathlib2, reducing dependencies for python 3
 - config file: 
   - use hashed (shorter) filename
   - resolve symlinks in file path
   - recognize `XDG_CONFIG_HOME` environment variable
 - move entry points, classifiers etc. to `setup.json` file

## [1.2.1] - 2018-06-11

### Changed
 - data file is now composed of the directory in which the python executable sits and the python major version (2 or 3)
 - setuptools relevant entry points can now be registered if specifically asked for
 - `PluginManager.scan`: `group_re` kwarg now allows string regex too
 - `PluginManager.iter_entry_points`: now scans by default if group or entry point not found
 - `PluginManager`: new constructor kwarg `scan_for_not_found` defaults to `True`, set to `False` to fail faster when no cached group / entry point is found.
 - `JsonBackend`, `BackendInterface`: The `write_*_dist()` methods have been replaced by `scan_*dist()`, the output of which can be passed to the `write_dist_map()` method.
 - `JsonBackend.epmap`: promoted to read-only property, returns copy of internal map.

## [1.2.0] - 2018-04-19

### Changed
 - data file name based on `sys.executable` to make sure entry points registered during install phase are available afterwards
 - `reentry_scan` during install no longer overwrites, but only adds (distributions installed simultaneously in one `pip` invocation can not discover each other's entry points and might overwrite each other)

### Added
 - setup coveralls
 - added coverage badge to REAME
 - cli: `reentry dev coveralls` runs coveralls only if TRAVIS env variable is set
 - read data dir from REENTRY_DATADIR env variable (env > rcfile > default)
 - CI test for registering entry points from the plugin host
 - documented limitations of `reentry_scan`
 - documented compatibility issues with `setup_requires`

## [1.1.2]

### Changed
 - fixed a bug that prevented from installing on windows

## [1.1.1]

### Changed
 - fixed a bug that prevented from installing in python 2.7 (added regression test)

## [1.1.0]

### Added
 - reentry now reads configuration from ~/.reentryrc or ~/.config/reentry/config if exists
 - configuration key: datadir, defaults to ~/.config/reentry/data/
 - entry points are now stored in a file in ~/.config/reentry/data/, named individually per installation
 - setup-hook `reentry_register` is now working and tested on Travis-CI
 - `reentry_register` now checks and does nothing if distribution has no entry points
 - setup-hook `reentry_scan` is now working and tested on Travis-CI

### Changed
 - reentry can now cache entry points even if the user has no write permission in it's install dir
 - JsonBackend API: small changes to the distribution writing methods

## [1.0.3]

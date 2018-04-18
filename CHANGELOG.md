# Changelog
All notable changes to this project after version 1.0.3 will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

## [1.2.0-alpha.1]

### Added
 - CI test for registering entry points from the plugin host

### Changed
 - change data file name to be based on `sys.executable` to make sure entry points registered during install phase are available afterwards

### Added
 - setup coveralls
 - added coverage badge to REAME
 - cli: `reentry dev coveralls` runs coveralls only if TRAVIS env variable is set

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

 ## [v1.0.3]

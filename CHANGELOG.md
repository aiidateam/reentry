# Changelog
All notable changes to this project after version 1.0.3 will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

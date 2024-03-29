.. image:: https://github.com/aiidateam/reentry/workflows/ci/badge.svg
    :target: https://github.com/aiidateam/reentry/actions

.. image:: https://codecov.io/gh/aiidateam/reentry/branch/develop/graph/badge.svg
   :target: https://codecov.io/gh/aiidateam/reentry

=======
Reentry
=======

A plugin manager based on setuptools entry points with 10x the speed

Archival notice
----------------

Python 3.8 saw the introduction of `importlib.metadata <https://docs.python.org/3/library/importlib.metadata.html>`_ into the Python standard library.
It is both fast to ``import importlib.metadata`` and fast to scan for entry points using the ``entry_points()`` function.

The separate `importlib-metadata <https://pypi.org/project/importlib-metadata/>`_ package backports this functionality to python >=3.6, and as of version 4.6.3 (or earlier), scanning is even faster than with the standard library.

Below are timings recorded on a MacBook Air M1 (2020) in a python 3.9.1 conda environment with 248 packages installed (~30 of which register entry points).

``pkg_resources``: ~147 msec in total::

    $ python -mtimeit -n1 -r1 'import pkg_resources'
    1 loop, best of 1: 146 msec per loop
    $ python -mtimeit -s 'import pkg_resources as pkg' 'pkg.iter_entry_points("aiida.calculations")'
    500000 loops, best of 5: 435 nsec per loop


``importlib.metadata``: ~39 msec in total::

    $ python -mtimeit -n1 -r1 'import importlib.metadata'
    1 loop, best of 1: 17.8 msec per loop
    $ python -mtimeit -s 'import importlib.metadata as im' 'im.entry_points()'
    50 loops, best of 5: 21.4 msec per loop

``importlib-metadata`` package (v4.6.3): ~40 msec in total::

    $ python -mtimeit -n1 -r1 'import importlib_metadata'
    1 loop, best of 1: 33.8 msec per loop
    $ python -mtimeit -s 'import importlib_metadata as im' 'im.entry_points()'
    50 loops, best of 5: 5.94 msec per loop

``reentry`` (v1.3.1): 25 msec in total::

    $ python -mtimeit -n1 -r1 'import reentry'
    1 loop, best of 1: 23.8 msec per loop
    $ python -mtimeit  -s 'from reentry.default_manager import PluginManager as p' 'p().get_entry_map()'
    200 loops, best of 5: 1.07 msec per loop

The advent of faster (solid-state) disks, together with the faster importlib implementations have led to a substantial reduction of the speed benefit that ``reentry`` provided (down to ~15 ms or ~40% in the benchmark above).
While there may still be certain edge cases where ``reentry`` is useful, we will stop using it going forward and are thus archiving this repository.

Users interested in continuing the maintenance of ``reentry`` are encouraged to open an issue on the issue tracker. 


Features
--------

* finding plugins: reentry keeps a map of entry points in a file
* speed: reentry provides an EntryPoint implementation that trades extra checks for search and load speed
* automatic registering: use ``reentry_register: True`` in your ``setup.py`` to automatically register plugins

Note that ``reentry_register`` creates a *build-time*
dependency on ``reentry``. The suggested way to resolve that is using the
method described in `PEP518 <https://www.python.org/dev/peps/pep-0518/>`_, for
which `support has been added in pip 10 <https://pip.pypa.io/en/latest/reference/pip/#pep-518-support>`_:
next to ``setup.py``, put a file ``pyproject.toml`` containing::

   [build-system]
   # Minimum requirements for the build system to execute.
   requires = ["setuptools", "wheel", "reentry"]

An alternative way for specifying a build dependency is to put::

   setup(
      ...
      setup_requires=[reentry],
      ...
   )

in your ``setup.py``.
This alternative works with all versions of ``pip``, but fails on systems,
where python is linked to old ``SSL`` libraries (such as the system python for
some versions of OS X).

Limitations
-----------

* entry points with extra dependencies (``name = module_name:attrs [extras]``)
  are still supported. Trying to load them, however, will lead to importing ``pkg_resources`` and
  forego the speedup.


Quickstart
----------

Use the following in your plugins's ``setup.py``::

   setup(
      ...
      setup_requires=['reentry'],
      reentry_register=True,
      entry_points={
         'my_plugins': ['this_plugin = this_package.subpackage:member'],
         ...
      }

And iterate over installed plugin from the host package::

   from reentry import manager
   available_plugins = manager.iter_entry_points(group='my_plugins')
   for plugin in available_plugins:
      plugin_object = plugin.load()
      plugin_object.use()

The syntax is consistent with ``setuptools``'s ``pkg_resources``, so you may use it as a fallback::

   try:
      from reentry import manager as entry_pt_manager
   except:
      import pkg_resources as entry_pt_manager

   entry_pt_manager.iter_entry_points(...)
   ...

Reentry Configuration
---------------------
Reentry supports getting information from a configuration file. The file will
be searched at the following paths:

* <HOME>/.reentryrc
* <HOME>/.config/reentry/config

The configuration file has an ``ini`` format and supports the following keys::

   [general]
   datadir=/path/to/data/dir
   data_filename=name

The ``datadir`` is the folder in which ``reentry`` stores the data file
that contains the information about the registered entry points.
If the config file doesn't exist in one of the above paths, the ``datadir`` is
set to ``<HOME>/.config/reentry/data``.
``data_filename`` is the name of the data file, in case you want to pick the
name by your own instead of letting ``reentry`` choose it.
Warning: By default, ``reentry`` creates a separate data file for every python
interpreter in order not to mix entry points between different python
environments on your system. Setting a ``data_filename`` in the configuration
file tells ``reentry`` to *always* use this data file and may result in
unexpected behavior if you use ``reentry`` in multiple python environments.

You can also set configuration options for ``reentry`` via environment
variables:

* ``datadir`` can be defined by ``REENTRY_DATADIR``.
* ``data_filename`` can be defined by ``REENTRY_DATA_FILENAME``.

Environment variables take precedence over the configuration file.

What for?
---------

To make entry points usable for plugins in time-critical situations such as
command line interfaces!

Setuptool's entry point system is convenient to use for plugin-based
python applications. It allows separate python packages to act as plugins
to a host package (or to each other), making it easy for the host to find and
iterate over the relevant data structures from plugins.

However, the time spent on importing `setuptools` scales badly with the
number of installed distributions and can easily reach 0.5 seconds for
moderately complex environments.
Finding and loading of plugins can be time-critical, for example in command
line tools that need to load subcommands, where 100 ms are a noticeable delay.

Importing setuptools's `pkg_resources` takes time, because it verifies that
dependencies are installed correctly for all distributions present in the
environment. This allows entry points to have additional dependencies or
"extras" (``entry_point = module_name:attrs [extras]``).

Reentry forgoes this dependency check for entry points without 'extras'
and thereby manages to be fast and scale better with the number
of plugins installed.

Standalone Manager Usage
------------------------

Sometimes it might be necessary to update the cached entry points, for example

* after uninstalling a plugin (there are no uninstall hooks by setuptools at the moment)
* after installing a plugin that does not use install hooks
* while developing a plugin / plugin host

for those cases reentry has a commandline interface::

   $ reentry --help
   Usage: reentry [OPTIONS] COMMAND [ARGS]...

     manage your reentry python entry point cache

   Options:
     --help  Show this message and exit.

   Commands:
     clear  Clear entry point map.
     dev    Development related commands.
     map    Print out a map of cached entry points
     scan   Scan for python entry points to cache for faster loading.

::

   $ reentry scan --help
   Usage: reentry scan [OPTIONS] PATTERN

      Scan for python entry points to cache for faster loading.

      Scan only for specific PATTERNs or leave empty to scan all

   Options:
      -r, --regex  Treat PATTERNs as regular expresions
      --help       Show this message and exit.

::

   $ reentry map --help
   Usage: reentry map [OPTIONS]

   Options:
     --dist TEXT   limit map to a distribution
     --group TEXT  limit map to an entry point group
     --name TEXT   limit map to entrypoints that match NAME
     --help        Show this message and exit.

Note: Where needed (e.g. in jupyter notebooks), these operations also be
performed in python using the reentry ``manager``, e.g.::

   from reentry import manager
   manager.scan()


CLI Example
-----------

Reentry provides a drop-in replacement for iter_entry_points::

   import click
   from click_plugins import with_plugins
   from reentry.manager import iter_entry_points

   @with_plugins(iter_entry_points('cli_plugins'))
   @click.group()
   def cli():
      """
      command with subcommands loaded from plugin entry points
      """

For this to work, reentry has to be installed and must have been used to
scan for entry points in the 'cli_plugins' group once.


Development 
-----------

Running the tests::

    tox

Creating a release::

    tox -e py39-release

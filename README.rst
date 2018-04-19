.. image:: https://travis-ci.org/DropD/reentry.svg?branch=master
    :target: https://travis-ci.org/DropD/reentry

.. image:: https://coveralls.io/repos/github/DropD/reentry/badge.svg
   :target: https://coveralls.io/github/DropD/reentry

=======
Reentry
=======

A plugin manager based on setuptools entry points with 10x the speed

Features
--------

* finding plugins: reentry keeps a map of entry points in a file
* speed: reentry provides an EntryPoint implementation that trades extras for search and load speed
* automatic registering: use ``reentry_register`` in your ``setup.py`` to automatically register plugins
* automatic scanning: use ``reentry_scan`` in your ``setup.py`` to automatically discover previously installed plugins

Note that ``reentry_register`` and ``reentry_scan`` create a build-time dependency on ``reentry``. The suggested way to resolve that is using the method described in `PEP518 <https://www.python.org/dev/peps/pep-0518/>`_, for which `support has been added in pip 10 <https://pip.pypa.io/en/latest/reference/pip/#pep-518-support>`_: next to ``setup.py``, put a file ``pyproject.toml`` containing::

   [build-system]
   # Minimum requirements for the build system to execute.
   requires = ["setuptools", "wheel", "reentry"]

An alternative way for specifying a build dependency is to put::

   setup(
      ...
      setup_requires=[reentry],
      ...
   )

in your ``setup.py``, this works with all versions of ``pip``, but fails on systems, where python is linked to old ``SSL`` libraries (like system python for some versions of OS X).

Limitations
-----------

* 
* entry points with extras dependencies still work trying to load them will lead to loading pkg_resources
* automatic scanning does not discover plugins installed during the same invocation of ``pip``::

   pip install plugin host

will not work, if ``plugin`` does not ``reentry_register``, and ``host`` does ``reentry_scan``, however::

   pip install plugin
   pip install host

Will work.

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

Note that the syntax is consistent with ``setuptools``'s ``pkg_resources``, so you may use it as a fallback::

   try:
      from reentry import manager as entry_pt_manager
   except:
      import pkg_resources as entry_pt_manager

   entry_pt_manager.iter_entry_points(...)
   ...

If your host package should search for entrypoints that were not installed using ``reentry_register``::

   # in host's setup.py
   setup(
      ...
      reentry_scan=['my_plugins', 'other_type_of_plugins']
      ...
   )

Note, that ``reentry_scan`` has to be a list, even if you only scan for one group.


What for?
---------

To make entry points usable for plugins in time-critical situations (like
commandline interfaces)!

Setuptool's entry point system is convenient to use for plugin based
python applications. It allows separate python packaes to act as plugins
to a host package, making it easy for the host to find and iterate over
the relevant data structures from plugins.

However simply importing setuptools scales badly with the number of installed
distributions and can be very slow for moderately complex environments (~ 0.5 s). 
Finding and loading of plugins on the other hand is time-critical in 
cases like commandline tools loading subcommands, where 100 ms are a noticeable
delay.

Setuptools's pkg_resources is slow, because it verifies dependencies are installed 
correctly for all distributions present in the environment on import. This allows
entry points to have additional requirements.

Reentry forgoes this dependency check for entry points without such 'extras'
dependencies and thereby manages to be fast and scale better, with the amount of
installed plugins, not installed python packages in general.

Standalone Manager Usage
------------------------

Sometimes it might be necessary to update the cached entry points, for example

   * after uninstalling a plugin (there are no uninstall hooks by setuptools atm)
   * after installing a plugin that does not use install hooks
   * while developping a plugin / plugin host

for those cases reentry has a commandline interface::

   $ reentry --help
   Usage: reentry [OPTIONS] COMMAND [ARGS]...
   
     manage your reentry python entry point cache
   
   Options:
     --help  Show this message and exit.
   
   Commands:
     map
     scan  Scan for python entry points to cache for...

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

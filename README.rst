=======
Reentry
=======

A plugin manager based on setuptools entry points with 10x the speed

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

Features
-----------------

* finding plugins: reentry keeps a map of entry points in a file
* speed: reentry provides an EntryPoint implementation that trades extras for search and load speed
* automatic registering: reentry provides setup() keyword args to register and scan for entry points on install
* flexible: entry points with extras dependencies still work trying to load them will lead to loading pkg_resources

Goal
====

Make an admin view to output the list of all installed packages with their
installed versions. Then we will be able to fix local installation from a
working instance when an unpinned package has been updated and contains backward
incompatibility.

Application must be easy to add to our projects so it could be quickly
deployed and definitively resolve futur issues with installations.

It must be qualitative since we don't want to introduce new bugs on currently
working projects.

The main challenge is the large environment diversity we have to support.

Constraints
===========

* Code quality;
* Simple;
* To work on almost all project environments, so Emansible and Buildout;
* Stable and large compatibility.

Environment supports
====================

Python
------

We plan for support from Python 2.7 to Python 3.6 (and further).

Django
------

We plan for support from Django 1.4 to Django 2.2 (and further).

Emansible
---------

Based on pip, it should be easy since pip API expose "freeze" without
backward incompatibility through its versions except a minor change on its
path.

A common way to reach freeze function with maximum compatibility: ::

    try:
        from pip._internal.operations import freeze
    except ImportError:  # pip < 10.0
        from pip.operations import freeze

    x = freeze.freeze()
    for p in x:
        print p

Buildout
--------

Since Buildout is based on Python Eggs installed through setuptools in a custom
directory ``eggs``, we can't use Pip.

But years ago we did a little script to get them and it was pretty stable to
use:

https://git.emencia.net/snippets/11

This should just have to be turned to a cleaner code embedded in a method
without global variables (moved as method arguments).

Output
======

Output will be pretty simple and identical for every package installer
wrapper. This should be a dict where item key is the package name and
item value is the version number as a string.

Sample: ::

    {
        "django": "1.6.11",
        "boussole": "0.5.1pre1",
    }

Roadmap
=======

1. Create package with basic structure including configuration for quality
   tools (pytest, flake8, tox).
2. Develop the core which will get the data about installed packages versions
   on every environment;
3. Enhance package structure to include tests about Django for every
   supported versions (through tox features);
4. Develop the Django admin view which will just use the package installer
   wrapper to output package datas;
5. Watch for an additional package installer wrapper bonus to use
   ``pipdeptree`` instead of pip freeze for compatible environments (obviously
   not for Buildout).

Ideas
=====

Package installer wrapper
-------------------------

Each one (Pip and Buildout) will just provide an output method to get the
package datas from installed project. They represent the core of this
application.

We will have an unified interface to get the informations: ::

    cooler = FreezeInfo(...)
    cooler.infos() # Will return OrderedDict


Testing
-------

Our tests will have to be fast (but still relevant) because we will have
something like a dozen Tox environments to cover.

We just need to test against our wrapper to be sure it returns an output
without any exception against environment diversity.

In a Test Driven Development goal, we will have distinct tests for pip and
buildout freeze and a last one for unified interface against available wrapper.

Tests will just check wrapper instance and output without to
bother about Python or pip versions.

Pip freeze
..........

Pip tests will use the package environment, no need to perform tests in
different virtual environments.

Buildout
........

Buildout tests will use a dummy ``eggs`` directory in test fixtures directory
since it won't work with our package environment. Dummy eggs should be enough
since Egg format is pretty stable.

Tox
...

Tox will run tests against Python and Django diversity throught
it's environments configurations.

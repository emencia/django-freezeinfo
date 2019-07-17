.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io
.. _sphinx-autobuild: https://github.com/GaretJax/sphinx-autobuild

===========
Development
===========

Development requirement
***********************

This application is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;

Every requirement is available in file ``requirements/development.txt``.

Install for development
***********************

First ensure you have `pip`_ and `virtualenv`_ package installed then type: ::

    git clone https://github.com/emencia/django-freezeinfo
    cd django-freezeinfo
    make install

Application will be installed in editable mode from the last commit on master branch.

Unittests
---------

Unittests are made to works on `Pytest`_, a shortcut in Makefile is available to start them on your current development install: ::

    make tests

Tox
---

To ease development against multiple Python versions a tox configuration has been added. You are strongly encouraged to use it to test your pull requests.

Before using it you will need to install tox, it is recommended to install it at your system level (tox dependancy is not in tests requirements file): ::

    sudo pip install tox>=3.4.0

Then go in the package directory ``django-freezeinfo`` and execute tox: ::

    tox

Workflow
********

Please, start every work inside a new branch for each feature. You will push it and merge it or create a pull request to request for validation with collaborators.

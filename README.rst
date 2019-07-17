.. _six: https://pypi.python.org/pypi/six
.. _Django: https://www.djangoproject.com/

Django Freeze info
==================

A Django application to output version information about every installed packages.

Links
*****

* Download his `PyPi package <https://pypi.python.org/pypi/django-freezeinfo>`_;
* Clone it on his `repository <https://github.com/emencia/django-freezeinfo>`_;

Requirements
************

* `six`_;
* `Django`_ >= 1.4;

Goal
****

Make an admin view to output the list of all installed packages with their
installed versions. Then we will be able to fix local installation from a
working instance when an unpinned package has been updated and contains backward
incompatibility.

Application must be easy to add to our projects so it could be quickly
deployed and definitively resolve futur issues with installations.

It must be qualitative since we don't want to introduce new bugs on currently
working projects.

The main challenge is the large environment diversity we have to support.

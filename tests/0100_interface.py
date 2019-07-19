import pytest
from collections import OrderedDict

from django_freezeinfo.info import FreezeInfo
from django_freezeinfo.errors import BuildoutError


def test_infos():
    """
    Front interface should get the right wrapper and return correct output
    without any errors.
    Returns:
        dict: Package name and number as a string.
    """

    # the test should return a dict if the path wasn't given and freeze
    # doesn't return the installed zc.buildout library from the pip wrapper
    # instance = FreezeInfo()
    # instance.infos()
    # assert isinstance(instance.infos(), OrderedDict)

    # the test should return a dictionary from the buildout wrapper
    # if the path was given
    # instance = FreezeInfo('eggs')
    # instance.infos()
    # assert isinstance(instance.infos(), OrderedDict)

    # the test should raise an error if the path wasn't given and freeze
    # returns the installed zc.buildout library from the pip wrapper
    # instance = FreezeInfo()
    # with pytest.raises(BuildoutError):
    #     instance.infos()

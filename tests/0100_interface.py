import pytest

from django_freezeinfo.info import FreezeInfo


def test_infos():
    """
    Front interface should get the right wrapper and return correct output
    without any errors.
    """
    instance = FreezeInfo()

    assert instance.infos() == {}

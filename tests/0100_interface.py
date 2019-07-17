import pytest

from django_freezeinfo import FreezeInfo


def test_output(db):
    """
    Front interface should get the right wrapper and return correct output
    without any errors.
    """
    instance = FreezeInfo()

    assert instance.output() == {}

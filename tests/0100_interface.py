import pytest

from django_freezeinfo.info import FreezeInfo


def test_infos():
    """
    Front interface should get the right wrapper and return correct output
    without any errors.
    """
    instance = FreezeInfo()

    # Temporary assertion until wrapper have been created and interface
    # connected
    with pytest.raises(NotImplementedError):
        instance.infos()

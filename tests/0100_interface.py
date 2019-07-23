import pytest
import json
from unittest import mock
from collections import OrderedDict

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from django_freezeinfo.info import FreezeInfo
from django_freezeinfo.errors import BuildoutError
from django_freezeinfo.views import info_view


PACKAGES = ['test_library==2.0.0', 'test_library2==1.0.0', 'test_library3']
PACKAGES_BUILDOUT = ['test_library==1.0.0', 'zc.buildout==1.0.0']

class InfoViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin_test')

    @mock.patch('django_freezeinfo.wrappers.pip_info.PACKAGES', iter(PACKAGES))
    def test_get_freeze_info_pip(self):
        '''Returns the pip information.
        The 'zc.buildout' library doesn't exist in the virtual enviroment,
        and a path was not transmitted.
        '''
        request = self.factory.get('/admin/freeze-info')
        request.user = self.user

        response = info_view(request)
        data = json.loads(response.content)
        self.assertEqual(type(data), dict)
        self.assertEqual(data.get('zc.buildout'), None)

    @mock.patch('django_freezeinfo.wrappers.pip_info.PACKAGES', iter(PACKAGES))
    def test_get_freeze_info_set_path(self):
        '''Returns the buildout information with an error.
        The 'zc.buildout' library doesn't exist in the virtual enviroment,
        and a path was transmitted.
        '''
        request = self.factory.get('/admin/freeze-info', {'path': 'eggs'})
        request.user = self.user

        response = info_view(request)
        data = json.loads(response.content)
        self.assertEqual(
            data, {'error': "[Errno 2] No such file or directory: 'eggs'"})

    @mock.patch(
        'django_freezeinfo.wrappers.pip_info.PACKAGES',
        iter(PACKAGES_BUILDOUT))
    def test_get_error_with_buildout_library(self):
        '''Returns the pip information with an error.
        The 'zc.buildout' library exists in the virtual enviroment,
        and a path was not transmitted.
        '''
        request = self.factory.get('/admin/freeze-info')
        request.user = self.user
        response = info_view(request)
        data = json.loads(response.content)
        self.assertEqual(type(data), dict)
        self.assertEqual(
            data, {'error': "The buildout wrapper needs an 'eggs' path."})

    @mock.patch(
        'django_freezeinfo.wrappers.pip_info.PACKAGES',
        iter(PACKAGES_BUILDOUT))
    def test_get_error_with_buildout_without_path(self):
        '''Returns the pip information with an error.
        The 'zc.buildout' library exists in the virtual enviroment,
        and a path was not transmitted.
        '''
        request = self.factory.get('/admin/freeze-info')
        request.user = self.user
        response = info_view(request)
        data = json.loads(response.content)
        self.assertEqual(type(data), dict)
        self.assertEqual(
            data, {'error': "The buildout wrapper needs an 'eggs' path."})


# def test_infos():
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

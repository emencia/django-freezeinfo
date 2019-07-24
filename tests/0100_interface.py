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
        request = self.factory.get('/admin/freeze-info', {'path': 'eggs-test'})
        request.user = self.user
        response = info_view(request)
        data = json.loads(response.content)
        self.assertEqual(
            data, {'error': "[Errno 2] No such file or directory: 'eggs-test'"})

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

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch(
        'django_freezeinfo.wrappers.pip_info.PACKAGES',
        iter(PACKAGES_BUILDOUT))
    def test_get_buildout_info_use_path(self, mocked_listdir, mocked_isdir, mocked_exist):
        '''Returns the buildout information.
        The 'zc.buildout' library exists in the virtual enviroment,
        and a path was transmitted.
        '''
        request = self.factory.get('/admin/freeze-info', {'path': 'eggs-test'})
        request.user = self.user
        mocked_listdir.return_value = ['bobo-2.4-test.egg']
        mocked_isdir.side_effect = [True]

        path = 'eggs-test/bobo-2.4-test.egg/EGG-INFO/requires.txt'

        with mock.patch("builtins.open", mock.mock_open(read_data=b'WebOb\nsix')) as mock_file:
            assert open(path).read() == b'WebOb\nsix'
            mock_file.assert_called_with(path)
            response = info_view(request)

        data = json.loads(response.content)
        self.assertEqual(type(data), dict)
        expected_data = {'bobo-2.4-test.egg': ['WebOb', 'six']}
        self.assertEqual(data, expected_data)

        mocked_listdir.return_value = ['WebOb-1.8-test-py3.6.egg']
        mocked_isdir.side_effect = [True]
        read_data = b'[docs]\nSphinx>=1.7.5\npylons-sphinx-themesn[testing]\ncoverage\npytest-cov\npytest>=3.1.0'
        path = 'eggs-test/WebOb-1.8-test-py3.6.egg/EGG-INFO/requires.txt'

        with mock.patch("builtins.open", mock.mock_open(read_data=read_data)) as mock_file:
            assert open(path).read() == read_data
            mock_file.assert_called_with(path)
            response = info_view(request)

        data = json.loads(response.content)
        self.assertEqual(type(data), dict)
        expected_data = {'WebOb-1.8-test-py3.6.egg': []}
        self.assertEqual(data, expected_data)


class InfosTest(TestCase):
    """
    Front interface should get the right wrapper and return correct output
    without any errors.
    Returns:
        dict: Package name and number as a string.
    """
    @mock.patch('django_freezeinfo.wrappers.pip_info.PACKAGES', iter(PACKAGES))
    def test_get_freeze_info_pip(self):
        '''Should return a dict if the path wasn't given and a freeze
        doesn't return the installed zc.buildout library from the pip wrapper.
        '''
        instance = FreezeInfo()
        data = instance.infos()
        self.assertEqual(type(data), OrderedDict)
        expected_data = {'test_library': '2.0.0', 'test_library2': '1.0.0'}
        self.assertEqual(data, expected_data)

    @mock.patch(
        'django_freezeinfo.wrappers.pip_info.PACKAGES',
        iter(PACKAGES_BUILDOUT))
    def test_get_error_with_buildout_library(self):
        '''Should raise an error if the path wasn't given and freeze
        returns the installed zc.buildout library from the pip wrapper.
        '''
        instance = FreezeInfo()
        with pytest.raises(BuildoutError):
            instance.infos()

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('django_freezeinfo.wrappers.pip_info.PACKAGES', iter(PACKAGES_BUILDOUT))
    def test_get_buildout_info_use_path(
            self, mocked_listdir, mocked_isdir, mocked_exist):
        '''Should return a dictionary from the buildout wrapper if the path
        was given.
        '''
        mocked_listdir.return_value = ['bobo-2.4-test.egg']
        mocked_isdir.side_effect = [True]

        path = 'eggs-test/bobo-2.4-test.egg/EGG-INFO/requires.txt'

        with mock.patch("builtins.open", mock.mock_open(read_data=b'WebOb\nsix')) as mock_file:
            self.assertEqual(open(path).read(), b'WebOb\nsix')
            mock_file.assert_called_with(path)
            instance = FreezeInfo('eggs-test')
            data = instance.infos()
            self.assertEqual(type(data), OrderedDict)
            expected_data = {'bobo-2.4-test.egg': ['WebOb', 'six']}
            self.assertEqual(data, expected_data)

        mocked_listdir.return_value = ['WebOb-1.8-test-py3.6.egg']
        mocked_isdir.side_effect = [True]
        read_data = b'[docs]\nSphinx>=1.7.5\npylons-sphinx-themesn[testing]\ncoverage\npytest-cov\npytest>=3.1.0'
        path = 'eggs-test/WebOb-1.8-test-py3.6.egg/EGG-INFO/requires.txt'

        with mock.patch("builtins.open", mock.mock_open(read_data=read_data)) as mock_file:
            self.assertEqual(open(path).read(), read_data)
            mock_file.assert_called_with(path)
            instance = FreezeInfo('eggs-test')
            data = instance.infos()
            self.assertEqual(type(data), OrderedDict)
            expected_data = {'WebOb-1.8-test-py3.6.egg': []}
            self.assertEqual(data, expected_data)

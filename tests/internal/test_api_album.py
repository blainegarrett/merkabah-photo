"""
Tests Surrounding Photo Album Api
"""

from mock import Mock, patch

from google.appengine.ext import ndb

from ...tests.internal.test_api import PhotoPluginApiCaseBase
from ...internal.api import album as api
from ...constants import PHOTOALBUM_KIND, PLUGIN_SLUG


class AlbumApiCaseBase(PhotoPluginApiCaseBase):
    """
    Base Test Case for Album Api helpers
    """
    pass


class GetAlbumKeyTests(AlbumApiCaseBase):
    """
    Tests surrounding getting album key
    """

    def test_base(self):
        test_slug = 'test'
        result_key = api.get_album_key(test_slug)

        self.assertTrue(isinstance(result_key, ndb.Key))
        self.assertEqual(result_key.kind(), PHOTOALBUM_KIND)

    def test_errors(self):
        """
        Ensure that passing in None or invalid types triggers errors
        """

        self.assertRaises(RuntimeError, api.get_album_key, None)
        self.assertRaises(RuntimeError, api.get_album_key, '')
        self.assertRaises(RuntimeError, api.get_album_key, {})
        self.assertRaises(RuntimeError, api.get_album_key, 612)

class GetAlbumKeyByKeyStrTests(AlbumApiCaseBase):
    """
    Tests surrounding getting the album key via urlsafe keystr
    """

    @patch('plugins.%s.internal.api.album.ndb' % PLUGIN_SLUG)
    def test_base(self, m_ndb):
        """
        Ensure our keystr helper wrapper calls the ndb.Key constructor correctly
        """

        # Setup Mocks
        m_key = Mock()
        m_key.kind.return_value = PHOTOALBUM_KIND
        m_key_init = Mock(name='mocked Key class', return_value=m_key)
        m_ndb.Key = m_key_init

        # Run code under test
        result = api.get_album_key_by_keystr('some_url_safe_keystr')

        # Check mocks
        self.assertEqual(result, m_key)
        m_key_init.assert_called_once_with(urlsafe='some_url_safe_keystr')

    def test_invalid_kind(self):
        """
        Ensure urlsafe keys from other Kinds do not work
        """

        bad_keystr = ndb.Key('SomeOtherKind', 612).urlsafe()
        self.assertRaises(RuntimeError, api.get_album_key_by_keystr, bad_keystr)

    def test_errors(self):
        """
        Ensure that passing in None or invalid types triggers errors
        """

        self.assertRaises(RuntimeError, api.get_album_key_by_keystr, None)
        self.assertRaises(RuntimeError, api.get_album_key_by_keystr, '')
        self.assertRaises(RuntimeError, api.get_album_key_by_keystr, 612)


class GetAlbumBySlugTests(AlbumApiCaseBase):
    """
    Tests surrounding getting album slug
    """

    @patch('plugins.%s.internal.api.album.get_album_key' % PLUGIN_SLUG)
    def test_base(self, m_get_album_key):
        # Setup Mocks
        test_slug = 'test'
        mock_key = Mock()
        mock_key.get = Mock(return_value='AlbumEntity') # Mock key.get() call

        m_get_album_key.return_value = mock_key

        # Run code under test
        result = api.get_album_by_slug(test_slug)

        # Check mocks
        m_get_album_key.assert_called_once_with('test')
        mock_key.get.assert_called_once_with()
        self.assertEqual(result, 'AlbumEntity')

    def test_errors(self):
        """
        Ensure that passing in None or invalid types triggers errors
        Note: We may want to eventually catch exception and return None
        """

        self.assertRaises(RuntimeError, api.get_album_by_slug, None)
        self.assertRaises(RuntimeError, api.get_album_by_slug, '')
        self.assertRaises(RuntimeError, api.get_album_by_slug, {})
        self.assertRaises(RuntimeError, api.get_album_by_slug, 612)


class CreateAlbumTests(AlbumApiCaseBase):
    pass


class EditAlbumTests(AlbumApiCaseBase):
    pass


class DeleteAlbumTests(AlbumApiCaseBase):
    pass


class FetchAlbumListTests(AlbumApiCaseBase):
    pass

"""
Tests Surrounding Photo Api
"""

from mock import Mock, patch, call

from google.appengine.ext import ndb

from ...tests.internal.test_api import PhotoPluginApiCaseBase
from ...internal.api import photo as api
from ...constants import PHOTOALBUM_KIND, PLUGIN_SLUG


class PhotoApiCaseBase(PhotoPluginApiCaseBase):
    """
    Base Test Case for Album Api helpers
    """
    pass


@patch('plugins.photo.internal.api.photo.get_photo_key')
class GetPhotoKeysByIdsTests(PhotoApiCaseBase):
    """
    Tests surrounding getting a list of photo entities by id
    """

    def test_base(self, m_get_photo_key):

        def _get_photo_key(photo_id):
            return photo_id

        m_get_photo_key.side_effect = _get_photo_key
        photo_ids = [6, 1, 2]
        result = api.get_photo_keys_by_ids(photo_ids)

        # Assert m_get_photo_key called the correct number of times with the correct args in order
        self.assertEqual(m_get_photo_key.call_count, 3)
        call_list = m_get_photo_key.call_args_list
        self.assertEqual(call_list[0], call(6))
        self.assertEqual(call_list[1], call(1))
        self.assertEqual(call_list[2], call(2))

        self.assertEqual(result, [6, 1, 2])


@patch('plugins.photo.internal.api.photo.ndb.get_multi')
@patch('plugins.photo.internal.api.photo.get_photo_keys_by_ids')
class GetPhotosByIdsTests(PhotoApiCaseBase):
    """
    Tests surrounding getting a list of photo entities by id
    """

    def test_base(self, m_get_photo_keys_by_ids, m_get_multi):
        m_get_photo_keys_by_ids.return_value = ['key6', 'key1', 'key2']
        m_get_multi.return_value = ['entity6', 'entity1', 'entity2']

        photo_ids = [6, 1, 2]
        result = api.get_photos_by_ids(photo_ids)

        m_get_photo_keys_by_ids.assert_called_once_with([6, 1, 2])
        m_get_multi.assert_called_once_with(['key6', 'key1', 'key2'])
        self.assertEqual(result, ['entity6', 'entity1', 'entity2'])

from __future__ import absolute_import

from google.appengine.ext import ndb

from ..constants import PHOTOALBUM_KIND, PHOTO_KIND


class Photo(ndb.Model):
    """
    A ndb.model wrapper to house a photo
    """
    title = ndb.StringProperty()
    caption = ndb.StringProperty()
    description = ndb.StringProperty()

    filename = ndb.StringProperty()
    content_type = ndb.StringProperty()
    gcs_filename = ndb.StringProperty()
    size = ndb.IntegerProperty()

    @property
    def size_in_kb(self):
        return self.size * 1000

    @classmethod
    def _get_kind(cls):
        return PHOTO_KIND # This can be overriden in the plugin.config


class PhotoAlbum(ndb.Model):
    """
    A ndb.model wrapper to house a photo
    """

    @classmethod
    def _get_kind(cls):
        return PHOTOALBUM_KIND # This can be overriden in the plugin.config

'''
class AlbumPhoto(ndb.Model):
    """
    A many to many interface
    """


class Collection(ndb.Model):
    """
    A ndb.model wrapper to house a photo
    """


class CollectionPhoto(ndb.Model):
    """
    A many to many interface
    """
'''

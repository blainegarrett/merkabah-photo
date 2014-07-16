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
    gcs_thumbnail_filename = ndb.StringProperty()
    gcs_sized_filename = ndb.StringProperty()    

    @property
    def size_in_kb(self):
        return self.size * 1000

    def get_thumbnail_url(self):
        return self.get_url('thumb')

    def get_sized_url(self):
        return self.get_url('sized')

    def get_full_url(self):
        return self.get_url('full')

    def get_url(self, version='thumb'):
        from merkabah import is_appspot, get_domain
        import settings

        if is_appspot():
            domain = 'commondatastorage.googleapis.com' #TODO: Make this definable in a setting
        else:
            domain = get_domain()

        bucket = settings.DEFAULT_GS_BUCKET_NAME

        if version == 'thumb':
            path = self.gcs_thumbnail_filename
        if version == 'sized':
            path = self.gcs_sized_filename
        if version == 'full':
            path = self.gcs_filename

        if not is_appspot():
            bucket = "_ah/gcs/%s" % bucket
        url = 'http://%s/%s/%s' % (domain, bucket, path)
        return url



    @classmethod
    def _get_kind(cls):
        return PHOTO_KIND # This can be overriden in the plugin.config


class PhotoAlbum(ndb.Model):
    """
    A ndb.model wrapper to house a photo
    """
    slug = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    photo_ids = ndb.IntegerProperty(repeated=True)

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

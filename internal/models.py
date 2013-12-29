from __future__ import absolute_import

import logging

from google.appengine.ext import ndb
from django.core import urlresolvers


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


class Album(ndb.Model):
    """
    A ndb.model wrapper to house a photo
    """


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

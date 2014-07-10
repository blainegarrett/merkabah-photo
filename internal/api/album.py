# Internal API Methods for Photo Albums
from google.appengine.ext import ndb
from ...internal.models import PhotoAlbum
from ...constants import PHOTOALBUM_KIND


def get_album_key_by_keystr(keystr):
    err = 'Keystrings must be an instance of base string, recieved: %s' % keystr

    if not keystr or not isinstance(keystr, basestring):
        raise RuntimeError(err)

    return ndb.Key(urlsafe=keystr)


def get_album_key(slug):
    """
    Create a ndb.Key given an Album slug
    """

    # TODO: Get Kind name off plugin def

    err = 'Series slug must be defined and of of type basestring'

    if not slug or not isinstance(slug, basestring):
        raise RuntimeError(err)

    return ndb.Key(PHOTOALBUM_KIND, slug)


def get_album_by_slug(slug):
    """
    Given an album slug, fetch the album entity
    """

    album_key = get_album_key(slug)
    album = album_key.get()
    return album


def edit_album(album_key, data, operator):
    """
    Edit a series
    """
    # TODO: This should be transactional
    # TODO: If slug changes, we need to update the key

    album = album_key.get()

    if not album:
        raise RuntimeError('Album could not be found by Key')

    for field, value in data.items():
        setattr(album, field, value)

    # Record audit, clear cache, etc
    album.put()

    return album


def delete_album(album_key, operator):
    """
    Delete a series
    """
    #TODO: Find all the artwork with this series and remove the series

    # Prep the file on cloud storage to be deleted
    album = album_key.get()

    if not album:
        raise RuntimeError('Album could not be found by Key')

    album_key.delete()
    return True


def get_series_list():
    """
    """

    # TODO: Paginate this, etc
    entities = PhotoAlbum.query().order(-PhotoAlbum.title).fetch(1000)

    return entities


def create_album(data, operator):
    """
    Create an Album
    """

    slug = data['slug']
    title = data['title']

    key = get_album_key(slug)
    entity = PhotoAlbum(key=key, slug=slug, title=title)
    entity.put()
    return entity

# Internal API Methods for Photo Albums
from google.appengine.ext import ndb
from ...internal.models import PhotoAlbum
from ...constants import PHOTOALBUM_KIND


def get_album_key_by_keystr(keystr):
    """
    Given a urlsafe version of an Album key, get the actual key
    """
    attr_err = 'Keystrings must be an instance of base string, recieved: %s' % keystr
    kind_err = 'Expected urlsafe keystr for kind %s but received keystr for kind %s instead.'
    if not keystr or not isinstance(keystr, basestring):
        raise RuntimeError(attr_err)

    key = ndb.Key(urlsafe=keystr)
    if not key.kind() == PHOTOALBUM_KIND:
        raise RuntimeError(kind_err % (PHOTOALBUM_KIND, key.kind()))

    return key


def get_album_key(slug):
    """
    Create a ndb.Key given an Album slug
    """
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

    data['photo_ids'] = [int(photo_id) for photo_id in data['photo_ids'].split(',') if photo_id]

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


def get_album_list():
    """
    Fetch a list of Albums
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
    description = data['description']

    photo_ids = data['photo_ids']
    photo_ids = [int(photo_id) for photo_id in photo_ids.split(',') if photo_id]

    key = get_album_key(slug)
    entity = PhotoAlbum(key=key, slug=slug, title=title, description=description, photo_ids=photo_ids)
    entity.put()
    return entity

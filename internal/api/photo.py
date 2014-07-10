from google.appengine.ext import ndb

from plugins.photo.internal.models import Photo, Album, Collection
from plugins.photo.constants import PHOTOS_PER_PAGE, ALBUMS_PER_PAGE, COLLECTIONS_PER_PAGE


# Photos
def get_photo_key_by_keystr(keystr):
    err = 'Keystrings must be an instance of base string, recieved: %s' % keystr

    if not keystr or not isinstance(keystr, basestring):
        raise RuntimeError(err)

    return ndb.Key(urlsafe=keystr)


def get_photo_key(id):
    """
    Create an ndb.Key given a photo id
    """

    # TODO: Get Kind name off plugin def

    err = 'Photo id must be defined and of of type int'

    if not id or not isinstance(slug, int):
        raise RuntimeError(err)

    return ndb.Key('Photo', id)


def get_photo_by_id(photo_id):
    """
    Given the id for a photo, attempt to fetch the Photo entity
    """
    key = get_photo_key(photo_id)
    return key.get()








def get_photos(cursor=None, limit=PHOTOS_PER_PAGE):
    """
    """
    pass


def get_albums(cursor=None, limit=ALBUMS_PER_PAGE):
    """
    """
    pass


def get_album_by_id(album_id):
    """
    Given the id for a Key, attempt to fetch the Album
    """
    key = ndb.Key('Album', album_id)
    return key.get()


def get_photos_by_album(collection_id):
    """
    """
    pass


def get_collections(cursor=None, limit=COLLECTIONS_PER_PAGE):
    """
    """
    pass


def get_collection_by_id(collection_id):
    """
    Given the id for a Key, attempt to fetch the Photo
    """
    key = ndb.Key('Collection', photo_id)
    return key.get()

def get_photos_by_collection(collection_id):
    """
    """

from plugins.photo.internal.models import Photo, Album, Collection
from plugins.photo.constants import PHOTOS_PER_PAGE, ALBUMS_PER_PAGE, COLLECTIONS_PER_PAGE


def get_photo_by_id(photo_id):
    """
    Given the id for a Key, attempt to fetch the Photo
    """
    key = ndb.Key('Photo', photo_id)
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

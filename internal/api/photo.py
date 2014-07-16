from merkabah.core.files.api.cloudstorage import Cloudstorage
from google.appengine.api import images

import logging
from google.appengine.ext import ndb

from plugins.photo.internal.models import Photo
from plugins.photo.constants import PHOTOS_PER_PAGE, ALBUMS_PER_PAGE, COLLECTIONS_PER_PAGE, PHOTO_KIND


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

    if not id or not isinstance(id, (int, long)):
        raise RuntimeError(err)

    return ndb.Key(PHOTO_KIND, id)


def get_photo_by_id(photo_id):
    """
    Given the id for a photo, attempt to fetch the Photo entity
    """
    key = get_photo_key(photo_id)
    return key.get()

def get_photo_keys_by_ids(photo_ids):
    key_list = []
    for photo_id in photo_ids:
        if not photo_id: # None, empty string, etc
            continue

        key_list.append(get_photo_key(photo_id))
    return key_list
    
def get_photos_by_ids(photo_ids):
    """
    Given a list of ids for photos, attempt to fetch the Photo entity
    """
    photo_keys = get_photo_keys_by_ids(photo_ids)
    photos = ndb.get_multi(photo_keys)
    return photos


def create_photo(slug, img_data, operator=None):
    content_type = 'image/jpeg'
    extension = 'jpg'

    # Store in cloud storage
    fs = Cloudstorage('dim-media') # Change to DefaultBucket

    # Regular Image

    # Note: This WILL Overwrite existing files...
    main_filename = 'photos/images/%s.%s' % (slug, extension)
    fs.write(main_filename, img_data, content_type)

    # Thumbnail
    file_content = rescale(img_data, 365, 235, halign='middle', valign='middle')
    thumbnail_filename = 'photos/thumbnail/%s.%s' % (slug, extension)
    logging.debug(thumbnail_filename)
    fs.write(thumbnail_filename, file_content, content_type)

    # Sized Images
    img = images.Image(img_data)
    img.resize(width=1000, height=1000)
    img.im_feeling_lucky()
    file_content = img.execute_transforms(output_encoding=images.JPEG)
    sized_filename = 'photos/sized/%s.%s' % (slug, extension)
    logging.debug(sized_filename)
    fs.write(sized_filename, file_content, content_type)

    photo = Photo()
    photo.filename = '%s.jpg' % slug
    photo.content_type = content_type
    photo.gcs_filename = main_filename
    photo.gcs_sized_filename = sized_filename
    photo.gcs_thumbnail_filename = thumbnail_filename
    photo.put()

    return photo


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
    key = ndb.Key('Collection', collection_id)
    return key.get()

def get_photos_by_collection(collection_id):
    """
    """

def rescale(img_data, width, height, halign='middle', valign='middle'):
  """Resize then optionally crop a given image.

  Attributes:
    img_data: The image data
    width: The desired width
    height: The desired height
    halign: Acts like photoshop's 'Canvas Size' function, horizontally
            aligning the crop to left, middle or right
    valign: Verticallly aligns the crop to top, middle or bottom

  """

  image = images.Image(img_data)      

  desired_wh_ratio = float(width) / float(height)
  wh_ratio = float(image.width) / float(image.height)

  if desired_wh_ratio > wh_ratio:
    # resize to width, then crop to height
    image.resize(width=width)
    image.execute_transforms()
    trim_y = (float(image.height - height) / 2) / image.height
    if valign == 'top':
      image.crop(0.0, 0.0, 1.0, 1 - (2 * trim_y))
    elif valign == 'bottom':
      image.crop(0.0, (2 * trim_y), 1.0, 1.0)
    else:
      image.crop(0.0, trim_y, 1.0, 1 - trim_y)
  else:
    # resize to height, then crop to width
    image.resize(height=height)
    image.execute_transforms()
    trim_x = (float(image.width - width) / 2) / image.width
    if halign == 'left':
      image.crop(0.0, 0.0, 1 - (2 * trim_x), 1.0)
    elif halign == 'right':
      image.crop((2 * trim_x), 0.0, 1.0, 1.0)
    else:
      image.crop(trim_x, 0.0, 1 - trim_x, 1.0)

  return image.execute_transforms()
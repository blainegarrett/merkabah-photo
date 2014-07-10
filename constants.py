"""
Default Photo Plugin Constants
"""

PHOTOS_PER_PAGE = 25
ALBUMS_PER_PAGE = 10 
COLLECTIONS_PER_PAGE = 10


from datetime import datetime
from settings import plugin_settings
import os

PLUGIN_SLUG = os.path.basename(os.path.dirname(__file__))

PHOTO_KIND = 'Photo'
PHOTOALBUM_KIND = 'PhotoAlbum'

try:
    PHOTO_KIND = plugin_settings[PLUGIN_SLUG]['PHOTO_KIND']
except KeyError:
    pass

try:
    PHOTOALBUM_KIND = plugin_settings[PLUGIN_SLUG]['PHOTOALBUM_KIND']
except KeyError:
    pass

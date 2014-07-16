"""
Merkabah Plugin to add Photo Galleries and Photo Collections
"""
import json

from google.appengine.ext import ndb
from plugins.photo.internal import api
from merkabah.core.controllers import TemplateResponse
from django.core import urlresolvers

from settings import DEFAULT_GS_BUCKET_NAME
from forms import PhotoAlbumForm
from merkabah.core.controllers import FormResponse
from django.http import HttpResponse, HttpResponseRedirect
import logging

from datatables import PhotoGrid, PhotoAlbumGrid
#from merkabah import get_domain

class PhotoPlugin(object):
    """
    """

    name = 'Photo Albums'
    entity_nice_name = 'photo'
    entity_plural_name = 'photo'

    def process_index(self, request, context, *args, **kwargs):
        """
        Driver switchboard logic
        """

        entities = api.photo.get_photos()
        context['grid'] = PhotoGrid(entities, request, context)
        return TemplateResponse('admin/plugin/index.html', context)

    def process_albums(self, request, context, *args, **kwargs):
        """
        Albums Index
        """
        from plugins.photo.internal.api import album as album_api

        entities = album_api.get_album_list()
        context['grid'] = PhotoAlbumGrid(entities, request, context)
        return TemplateResponse('admin/plugin/index.html', context)

    def process_create_album(self, request, context, *args, **kwargs):
        """
        Handler for creating an album
        """
        from plugins.photo.internal.api import album as album_api

        form = PhotoAlbumForm()
        setattr(form, 'domain_root', request.META['HTTP_HOST'])

        context['form'] = form

        if request.POST:
            context['form'] = PhotoAlbumForm(request.POST)
            if context['form'].is_valid():
                form_data = context['form'].cleaned_data
                album = album_api.create_album(form_data, operator=None) #TODO: Add operator
                return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'albums')))

        return FormResponse(form, id='album_create_form', title="Create", target_url=urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'create_album')), target_action='create_album', template='plugins/photo/admin/album_form.html')

    def process_edit_album(self, request, context, *args, **kwargs):
        """
        Handler for editing a series
        """
        from plugins.photo.internal.api import album as album_api

        album_keystr = request.REQUEST['album_key']

        if not album_keystr:
            raise RuntimeError('No argument post_key provided.')

        album_key = album_api.get_album_key_by_keystr(album_keystr)
        album = album_key.get() # TODO: Make into api method

        initial_data = {
            'slug': album.slug,
            'title': album.title,
            'description': album.description
        }

        initial_data['photo_ids'] = ','.join([str(photo_id) for photo_id in album.photo_ids if photo_id])

        form = PhotoAlbumForm(initial=initial_data)
        setattr(form, 'domain_root', request.META['HTTP_HOST'])

        #Refactor this HARD
        setattr(form, 'photo_entities', [])        
        form.photo_entities = [ndb.Key('DimPhoto', photo_id).get() for photo_id in album.photo_ids if photo_id]

        context['form'] = form

        if request.POST:
            context['form'] = PhotoAlbumForm(request.POST)
            if context['form'].is_valid():
                form_data = context['form'].cleaned_data
                album = album_api.edit_album(album_key, form_data, operator=None) #TODO: Add operator
                return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'albums')))

        target_url = "%s?album_key=%s" % (urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'edit_album')), album_key.urlsafe())
        return FormResponse(form, id='album_edit_form', title="Edit", target_url=target_url, target_action='edit_album', template='plugins/photo/admin/album_form.html')

    def process_delete_album(self, request, context, *args, **kwargs):
        """
        Handler for deleting an album
        """
        from plugins.photo.internal.api import album as album_api

        # TODO: Need to handle confirmation

        album_keystr = request.REQUEST['album_key']

        if not album_keystr:
            raise RuntimeError('No argument album_key provided.')

        album_key = album_api.get_album_key_by_keystr(album_keystr)

        # Call api to delete series, etc
        album_api.delete_album(album_key, operator=None)

        return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'albums')))

    def process_photo_upload_json(self, request, context, *args, **kwargs):
        kwargs['give_me_json_back'] = True # Hacky but will have to do until we have a betterway

        return self.process_photo_create(request, context, *args, **kwargs)

    def process_get_upload_url(self, request, context, *args, **kwargs):
        upload_url = api.create_upload_url(request.POST['callback'])
        response_dict = {'url': upload_url}
        return HttpResponse(json.dumps(response_dict))


    def process_photo_create(self, request, context, *args, **kwargs):
        """
        Upload a new image to an Album
        """

        from merkabah.core.files.api.cloudstorage import Cloudstorage
        from google.appengine.ext import blobstore
        from plugins.photo.internal.api.photo import create_photo

        # Get the file upload url

        fs = Cloudstorage(DEFAULT_GS_BUCKET_NAME)

        #form = ImageUploadForm()

        #context['form'] = form
        has_files = fs.get_uploads(request, 'the_file', True)


        if has_files:
            file_info = has_files[0]

            original_filename = file_info.filename
            content_type = file_info.content_type
            size = file_info.size
            gs_object_name = file_info.gs_object_name # Using this we could urlfetch, but the file isn't public...
            blob_key = blobstore.create_gs_key(gs_object_name)
            logging.warning(blob_key)
            data =  fs.read(gs_object_name.replace('/gs', ''))

            slug = original_filename.split('.')[0] # I dislike this..

            photo = create_photo(slug, data)

            # What we want to do now is create a copy of the file with our own info

            dest_filename = '%s' % original_filename

            new_gcs_filename = fs.write(dest_filename, data, content_type)
            logging.warning(new_gcs_filename)

            # Finally delete the tmp file
            data =  fs.delete(gs_object_name.replace('/gs', ''))

            if not kwargs.get('give_me_json_back'):
                return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'images')))

            # Else... we're hacky emulating an upload rest endpoint - return json info about the image
            response_dict = {
                'cool': True,
                'photo_id': photo.key.id(),
                'keystr': photo.key.urlsafe(),
                'filename': photo.filename,
                'thumbnail_url': photo.get_thumbnail_url()
            }

            return HttpResponse(json.dumps(response_dict))

        #upload_url = fs.create_upload_url('/madmin/plugin/artwork/images_create/')
        #return FormResponse(form, id='images_create_form', title="Upload a file", target_url=upload_url, target_action='images_create', is_upload=True)


# Register Plugin
pluginClass = PhotoPlugin
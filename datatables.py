from merkabah.core import datatable as merkabah_datatable
from django.core import urlresolvers

# Photo DataTables

class PhotoGroupActions(object):
    """
    """

    def render_content(self, context):
        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'create'))
        return '<a href="%s" class="btn-primary btn">Create</a>' % link


class PhotoActionColumn(merkabah_datatable.DatatableColumn):
    """
    """

    def render_content(self, obj, context):

        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'edit'))
        link = '%s?artwork_key=%s' % (link, obj.key.urlsafe())
        output = '<a href="%s" class="btn btn-default">Edit</a>' % link

        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'delete'))
        link = '%s?artwork_key=%s' % (link, obj.key.urlsafe())
        output += '<a href="%s" class="btn btn-default">Delete</a>' % link
        return output


class PhotoGrid(merkabah_datatable.Datatable):
    """
    """

    title = merkabah_datatable.DatatableColumn()
    slug = merkabah_datatable.DatatableColumn()
    content = merkabah_datatable.DatatableColumn()
    published_date = merkabah_datatable.DatatableColumn()
    created_date = merkabah_datatable.DatatableColumn()
    modified_date = merkabah_datatable.DatatableColumn()
    series = merkabah_datatable.DatatableColumn()
    primary_media_image = merkabah_datatable.DatatableColumn()
    attached_media = merkabah_datatable.DatatableColumn()
    height = merkabah_datatable.DatatableColumn()
    width = merkabah_datatable.DatatableColumn()
    year = merkabah_datatable.DatatableColumn()

    # Some quicky versions of 
    sale = merkabah_datatable.DatatableColumn()
    price = merkabah_datatable.DatatableColumn()
    
    actions = PhotoActionColumn()
    group_actions = PhotoGroupActions()
    column_order = ['title', 'slug', 'published_date', 'created_date', 'series', 'primary_media_image', 'attached_media', 'height', 'width', 'year', 'sale', 'price', 'actions']



# Photo Image Datatables
class PhotoMediaThumbnailColumn(merkabah_datatable.DatatableColumn):
    """
    """

    def render_content(self, obj, context):
        """
        """

        img_url = obj.get_thumbnail_url()

        output = '<a href="%s"><img class="thumbnail" src="%s" style="max-width:300px;max-height:200px;" alt="Placeholder Image" /></a>' % (img_url, img_url)
        return output


class PhotoImageGroupActions(object):
    """
    """

    def render_content(self, context):
        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'images_create'))
        return '<a href="%s" class="btn-primary btn">Create</a>' % link


class PhotoImageGrid(merkabah_datatable.Datatable):
    thumb = PhotoMediaThumbnailColumn()
    filename = merkabah_datatable.DatatableColumn()
    blob_key = merkabah_datatable.DatatableColumn()
    gcs_filename = merkabah_datatable.DatatableColumn()
    gcs_thumbnail_filename = merkabah_datatable.DatatableColumn()
    gcs_sized_filename = merkabah_datatable.DatatableColumn()
    content_type = merkabah_datatable.DatatableColumn()
    size = merkabah_datatable.DatatableColumn()
    group_actions = PhotoImageGroupActions()
    column_order = ['thumb', 'filename', 'blob_key', 'gcs_filename', 'content_type', 'size']


# Series Datatables
class PhotoAlbumActions(object):
    """
    """

    def render_content(self, context):
        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'create_album'))
        output = '<a href="%s" class="btn-primary btn">Create</a>&nbsp;&nbsp;&nbsp;' % link
        return output


class PhotoAlbumActionColumn(merkabah_datatable.DatatableColumn):
    """
    """

    def render_content(self, obj, context):

        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'edit_album'))
        link = '%s?album_key=%s' % (link, obj.key.urlsafe())
        output = '<a href="%s" class="btn btn-default">Edit</a>' % link

        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'delete_album'))
        link = '%s?album_key=%s' % (link, obj.key.urlsafe())
        output += '<a href="%s" class="btn btn-default">Delete</a>' % link
        return output


class PhotoAlbumGrid(merkabah_datatable.Datatable):
    # Column Definitions
    title = merkabah_datatable.DatatableColumn()
    slug = merkabah_datatable.DatatableColumn()
    actions = PhotoAlbumActionColumn()

    column_order = ['title', 'slug', 'actions']

    group_actions = PhotoAlbumActions()

    def get_row_identifier(self, obj):
        return obj.key.urlsafe()

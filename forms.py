from merkabah.core import forms as merkabah_forms
from django import forms

class PhotoAlbumForm(merkabah_forms.MerkabahBaseForm):
    """
    Form for Creatuing and Editing a Series
    """

    title = forms.CharField(label='Title', max_length=100, required=True)
    slug = forms.CharField(label='Slug', max_length=100, required=True)
    description = forms.CharField(label='Content', required=False, widget=forms.Textarea(attrs={'placeholder': 'Content', 'class': 'cxxkeditor'}))
    photo_ids = forms.CharField(label='Photos', required=True)
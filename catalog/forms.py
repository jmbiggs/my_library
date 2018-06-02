from django import forms
from django.forms import ModelForm

from .models import Item, Patron, Authorship, Author

from dal import autocomplete

class SearchModeForm(forms.Form):
	SEARCH_MODES = (
		('item', 'Item'),
		('patron', 'Patron'),
	)
	
	mode = forms.ChoiceField(label='', choices=SEARCH_MODES)

class SearchForm(forms.Form):
	query = forms.CharField(label='', max_length=100, required=False)
	
class PatronForm(forms.ModelForm):
	class Meta:
		model = Patron
		fields = ['patron_name', 'email']

class AuthorshipForm(forms.ModelForm):
	author = forms.ModelChoiceField(
		queryset=Author.objects.all(),
		required=False,
		widget=autocomplete.ModelSelect2(url='author-autocomplete')
	)
	
	def is_blank(self):
		author_blank = self.cleaned_data.get('author') is None
		author_type_blank = self.cleaned_data.get('author_type') is None
		
		return author_blank or author_type_blank
	
	class Meta:
		model = Authorship
		fields = ['author', 'author_type']
#		widgets = {
#					'author': autocomplete.ModelSelect2(url='author-autocomplete')
#					}

class ItemForm(forms.ModelForm):	
	class Meta:
		model = Item
		fields = ['media_type', 'title', 'shelf_location', 'publication_date', 'catalog_id', 'isbn', 'upc', 'condition', 'notes', 'lost', 'api_link']
		widgets = {
			'media_type': forms.Select(attrs={'onchange': 'display_authors(this)', 'class': 'media_form'}),
		}

#	def save(self, commit=True):
#		return super(ItemForm, self).save(commit=commit)

#, 'aquisition_date', 'last_modified_date',

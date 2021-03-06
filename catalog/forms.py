from django import forms
from django.forms import ModelForm

from .models import Item, Patron, Author

class SearchModeForm(forms.Form):
	SEARCH_MODES = (
		('item', 'Item'),
		('patron', 'Patron'),
	)
	
	mode = forms.ChoiceField(label='', choices=SEARCH_MODES)

class SearchForm(forms.Form):
	query = forms.CharField(label='', max_length=100, required=False)
	
class PatronForm(ModelForm):
	class Meta:
		model = Patron
		fields = ['patron_name', 'email']

class ItemForm(ModelForm):
	class Meta:
		model = Item
		fields = ['media_type', 'catalog_id', 'isbn', 'upc', 'condition', 'notes', 'title', 'authors', 'shelf_location', 'publication_date', 'lost', 'api_link']

#, 'aquisition_date', 'last_modified_date',
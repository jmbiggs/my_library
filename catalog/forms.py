from django import forms

class PatronSearchForm(forms.Form):
	query = forms.CharField(label='Patron search', max_length=100)

class PatronSearchTypeForm(forms.Form):
	SEARCH_TYPES = (
		('name', 'Name'),
		('email', 'Email Address'),
		('id', 'Patron ID #'),
	)
	
	query_type = forms.ChoiceField(label='', choices=SEARCH_TYPES)

class ItemSearchForm(forms.Form):
	query = forms.CharField(label='Item search', max_length=100)
	
class ItemSearchTypeForm(forms.Form):
	SEARCH_TYPES = (
		('title', 'Title'),
		('author', 'Person'),
		('type', 'Media Type'),
		('id', 'Item ID #'),
	)
	
	query_type = forms.ChoiceField(label='', choices=SEARCH_TYPES)
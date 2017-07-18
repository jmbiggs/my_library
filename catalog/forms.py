from django import forms

class PatronSearchForm(forms.Form):
	p_query = forms.CharField(label='Patron search', max_length=100)

class PatronSearchTypeForm(forms.Form):
	SEARCH_TYPES = (
		('name', 'Name'),
		('email', 'Email Address'),
		('id', 'Patron ID #'),
	)
	
	p_query_type = forms.ChoiceField(label='', choices=SEARCH_TYPES)

class ItemSearchForm(forms.Form):
	i_query = forms.CharField(label='Item search', max_length=100)
	
class ItemSearchTypeForm(forms.Form):
	SEARCH_TYPES = (
		('title', 'Title'),
		('author', 'Person'),
		('type', 'Media Type'),
		('id', 'Item ID #'),
	)
	
	i_query_type = forms.ChoiceField(label='', choices=SEARCH_TYPES)
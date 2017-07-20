from django import forms

class SearchModeForm(forms.Form):
	SEARCH_MODES = (
		('item', 'Item'),
		('patron', 'Patron'),
	)
	
	mode = forms.ChoiceField(label='', choices=SEARCH_MODES)

class SearchForm(forms.Form):
	query = forms.CharField(label='', max_length=100)

from django import forms

class PatronSearchForm(forms.Form):
	patron_query = forms.CharField(label='Patron name', max_length=100)

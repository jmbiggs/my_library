# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .forms import PatronSearchForm, PatronSearchTypeForm
from .models import Item, Patron, Author, CheckOut

def index(request):
	context = {}
	return render(request, 'catalog/index.html', context)
	
def browse(request):
	items = Item.objects.all()
	context = {'item_list': items}
	return render(request, 'catalog/browse.html', context)
	
def item_record(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	checkouts = CheckOut.objects.filter(item_id=item_id).filter(check_in_date__isnull=True)
	context = {'item': item, 'checkouts': checkouts}
	return render(request, 'catalog/item.html', context)

def patron_lookup(request):
	patron_query = request.GET.get('query')
	patron_query_type = request.GET.get('query_type')
	if patron_query is not None:
		form = PatronSearchForm({'query':patron_query})
		type_form = PatronSearchTypeForm({'query_type':patron_query_type})
		
		# run search query
		if patron_query_type == 'name':
			query_results = Patron.objects.filter(patron_name__icontains=patron_query)
		elif patron_query_type == 'email':
			query_results = Patron.objects.filter(email__icontains=patron_query)
		elif patron_query_type == 'id':
			if is_int(patron_query):
				query_results = Patron.objects.filter(pk=patron_query)
			else:
				query_results = Patron.objects.none()
		
		context = {'form': form, 'type_form': type_form, 'patron_query': patron_query, 'query_results': query_results}
	else:
		form = PatronSearchForm()
		type_form = PatronSearchTypeForm()
		context = {'form': form, 'type_form': type_form}

	return render(request, 'catalog/patron.html', context)
	
def patron_record(request, patron_id):
	patron = get_object_or_404(Patron, pk=patron_id)
	current_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=True)
	old_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=False)
	
	context = {'patron': patron, 'current_checkouts': current_checkouts, 'old_checkouts': old_checkouts}
	return render(request, 'catalog/patron_record.html', context)

# helpers

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	
	
	
	
	
	
	
	
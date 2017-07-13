# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .forms import PatronSearchForm, PatronSearchTypeForm, ItemSearchForm, ItemSearchTypeForm
from .models import Item, Patron, Author, CheckOut

def index(request):
	context = {}
	return render(request, 'catalog/index.html', context)
	
def browse(request):
	# get possible queries
	query = request.GET.get('i_query')
	query_type = request.GET.get('i_query_type')
	if query is not None:
		form = ItemSearchForm({'i_query': query})
		type_form = ItemSearchTypeForm({'i_query_type': query_type})
		
		# run search query
		query_results = item_query(query, query_type)
			
		context = {'form': form, 'type_form': type_form, 'query_results': query_results}
	else:
		form = ItemSearchForm()
		type_form = ItemSearchTypeForm()
		items = Item.objects.all()
		context = {'query_results': items, 'form': form, 'type_form': type_form}
	return render(request, 'catalog/browse.html', context)
	
def item_record(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	checkouts = CheckOut.objects.filter(item_id=item_id).filter(check_in_date__isnull=True)
	context = {'item': item, 'checkouts': checkouts}
	return render(request, 'catalog/item.html', context)

def patron_lookup(request):
	query = request.GET.get('p_query')
	query_type = request.GET.get('p_query_type')
	if query is not None:
		form = PatronSearchForm({'p_query': query})
		type_form = PatronSearchTypeForm({'p_query_type': query_type})
		
		# run search query
		query_results = patron_query(query, query_type)
				
		context = {'form': form, 'type_form': type_form, 'query_results': query_results}
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

def checkout(request):
	# get possible info passed to url
	item_id = request.GET.get('item')
	i_query = request.GET.get('i_query')
	i_query_type = request.GET.get('i_query_type')
	patron_id = request.GET.get('patron')
	p_query = request.GET.get('p_query')
	p_query_type = request.GET.get('p_query_type')
	
	# default context objects
	item = None
	item_form = None
	item_type_form = None
	item_results = None
	patron = None
	patron_form = None
	patron_type_form = None
	patron_results = None
	
	# item section	
	if item_id is None:
		if i_query is None:
			item_form = ItemSearchForm()
			item_type_form = ItemSearchTypeForm()
		else:
			item_results = item_query(i_query, i_query_type)
			item_form = ItemSearchForm({'i_query': i_query})
			item_type_form = ItemSearchTypeForm({'i_query_type': i_query_type})
	else:
		item = get_object_or_404(Item, pk=item_id)
		
	# patron section
	if patron_id is None:
		if p_query is None:
			patron_form = PatronSearchForm()
			patron_type_form = PatronSearchTypeForm()
		else:
			patron_results = patron_query(p_query, p_query_type)
			patron_form = PatronSearchForm({'p_query': p_query})
			patron_type_form = PatronSearchTypeForm({'p_query_type': p_query_type})
	else:
		patron = get_object_or_404(Patron, pk=patron_id)
		
	context = {'item': item, 'item_form': item_form, 'item_type_form': item_type_form, 'item_results': item_results, 'patron': patron, 'patron_form': patron_form, 'patron_type_form': patron_type_form, 'patron_results': patron_results}

	return render(request, 'catalog/checkout.html', context)

def checkin(request):
	context = {}
	return render(request, 'catalog/checkin.html', context)

# helpers

def patron_query(query, query_type):
	if query_type == 'name':
		return Patron.objects.filter(patron_name__icontains=query)
	elif query_type == 'email':
		return Patron.objects.filter(email__icontains=query)
	elif query_type == 'id':
		if is_int(query):
			return Patron.objects.filter(pk=query)
		else:
			return Patron.objects.none()

def item_query(query, query_type):
	if query_type == 'title':
		return Item.objects.filter(title__icontains=query)
	elif query_type == 'author':
		return Item.objects.filter(authors__author_name__icontains=query)			
	elif query_type == 'type':
		return Item.objects.filter(media_type__icontains=query)			
	elif query_type == 'id':
		if is_int(query):
			return Item.objects.filter(pk=query)
		else:
			return Item.objects.none()

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	
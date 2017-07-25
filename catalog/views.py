# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .forms import SearchModeForm, SearchForm, PatronForm, ItemForm
from .models import Item, Patron, Author, CheckOut

def index(request):
	# get possible parameters passed to url
	search_mode = request.GET.get('mode')
	query = request.GET.get('query')
	item_id = request.GET.get('item')
	patron_id = request.GET.get('patron')
	
	if item_id is not None:
		item = get_object_or_404(Item, pk=item_id)
	else:
		item = None
		
	if patron_id is not None:
		patron = get_object_or_404(Patron, pk=patron_id)			
	else:
		patron = None
			
	if search_mode is None:
		if item is not None:
			search_mode = 'patron'
		else:
			search_mode = 'item'
	mode_form = SearchModeForm({'mode': search_mode})

	if query is None:
		search_form = SearchForm()
		results = None
	else:
		search_form = SearchForm({'query': query})
		if search_mode == 'patron':
			results = patron_query(query)
		else:
			results = item_query(query)
	
	context = {'mode': search_mode, 'mode_form': mode_form, 'search_form': search_form, 'item': item, 'results': results, 'patron': patron}

	return render(request, 'catalog/index.html', context)

def new_item(request):
	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			form.save()
			updated = True
		else:
			updated = False
	else:	
		form = ItemForm()
		updated = None
		
	context = {'form': form, 'updated': updated}
	return render(request, 'catalog/item.html', context)

def item_record(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	
	if request.method == 'POST':
		form = ItemForm(request.POST, instance=item)
		if form.is_valid():
			form.save()
			updated = True
		else:
			updated = False

	else:
		form = ItemForm(instance=item)
		updated = None
	
	checkouts = CheckOut.objects.filter(item_id=item_id).filter(check_in_date__isnull=True)
	
	context = {'item': item, 'form': form, 'updated': updated, 'checkouts': checkouts}
	return render(request, 'catalog/item.html', context)
	
def new_patron(request):
	if request.method == 'POST':
		form = PatronForm(request.POST)
		if form.is_valid():
			form.save()
			updated = True
		else:
			updated = False
	else:	
		form = PatronForm()
		updated = None

	context = {'form': form, 'updated': updated}
	return render(request, 'catalog/patron_record.html', context)
	
def patron_record(request, patron_id):
	patron = get_object_or_404(Patron, pk=patron_id)
	
	if request.method == 'POST':
		form = PatronForm(request.POST, instance=patron)
		if form.is_valid():
			form.save()
			updated = True
		else:
			updated = False
	else:
		form = PatronForm(instance=patron)
		updated = None

	current_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=True)
	old_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=False)
	
	context = {'patron': patron, 'form': form, 'updated': updated, 'current_checkouts': current_checkouts, 'old_checkouts': old_checkouts}
	return render(request, 'catalog/patron_record.html', context)

# helpers

def patron_query(query):
	if query == '':
		return Patron.objects.all()
	
	if is_int(query):
		id_query = Q(pk=query)
	else:
		id_query =  Q()

	name_query = Q(patron_name__icontains=query)
	email_query = Q(email__icontains=query)
	return Patron.objects.filter(id_query | name_query | email_query).distinct()
	
def item_query(query):
	if query == '':
		return Item.objects.all()
	
	if is_int(query):
		id_query = Q(pk=query)
	else:
		id_query = Q()

	title_query = Q(title__icontains=query)
	author_query = Q(authors__author_name__icontains=query)			
	return Item.objects.filter(id_query | title_query | author_query).distinct()

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .forms import SearchModeForm, SearchForm
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

def item_record(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	checkouts = CheckOut.objects.filter(item_id=item_id).filter(check_in_date__isnull=True)
	
	context = {'item': item, 'checkouts': checkouts}
	return render(request, 'catalog/item.html', context)
	
def patron_record(request, patron_id):
	patron = get_object_or_404(Patron, pk=patron_id)
	current_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=True)
	old_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=False)
	
	context = {'patron': patron, 'current_checkouts': current_checkouts, 'old_checkouts': old_checkouts}
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

#def item_record(item):
#	id_str = "ID: " + item.id + "\n" 
#	title_str = "TITLE: " + item.title + "\n"
#	authors_str = ""	
#	for author in item.authors.all:
#		authors_str += author.author_type + ": " + author.author_name + "\n"
#	media_str = "MEDIA TYPE: " + item.media_type + "\n"
#		
#	checkouts_str = ""
#	checkouts = CheckOut.objects.filter(item_id=item_id).filter(check_in_date__isnull=True)
#	if (checkouts.exists()):
#		checkouts_str += "\n"
#		# note: there should only be at most one checkout, but i'm putting this here in case something goes wrong so that it will be visible
#		for checkout in checkouts:
#			checkouts_str += "CHECKED OUT TO: " + checkout.patron.patron_name  + "(due date: " + checkout.due_date + ")\n"
##<a href="{% url 'patron_record' checkout.patron.id %}">{{

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	
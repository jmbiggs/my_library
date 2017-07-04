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
	item_query = request.GET.get('query')
	item_query_type = request.GET.get('query_type')
	if item_query is not None:
		form = ItemSearchForm({'query': item_query})
		type_form = ItemSearchTypeForm({'query_type': item_query_type})
		
		# run search query
		if item_query_type == 'title':
			query_results = Item.objects.filter(title__icontains=item_query)
		elif item_query_type == 'author':
			query_results = Item.objects.filter(authors__author_name__icontains=item_query)			
		elif item_query_type == 'type':
			query_results = Item.objects.filter(media_type__icontains=item_query)			
		elif item_query_type == 'id':
			if is_int(item_query):
				query_results = Item.objects.filter(pk=item_query)
			else:
				query_results = Item.objects.none()
			
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
	patron_query = request.GET.get('query')
	patron_query_type = request.GET.get('query_type')
	if patron_query is not None:
		form = PatronSearchForm({'query': patron_query})
		type_form = PatronSearchTypeForm({'query_type': patron_query_type})
		
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
	# to complete checkout we need item and patron
	item_id = request.GET.get('item')
	patron_id = request.GET.get('patron')
	
	# if we have neither:
	if item_id is None and patron_id is None:
		patron_form = PatronSearchForm()
		patron_type_form = PatronSearchTypeForm()
		context = {'patron_form': patron_form, 'patron_type_form': patron_type_form}
		
	# if we have patron, but not item:
	elif item_id is None and patron_id is not None:
		patron = get_object_or_404(Patron, pk=patron_id)
		context = {'patron': patron}
		
	# if we have item, but not patron:
	elif item_id is not None and patron_id is None:
		item = get_object_or_404(Item, pk=item_id)
		patron_search_form = PatronSearchForm()
		patron_search_type_form = PatronSearchTypeForm()
		context = {'item': item, 'patron_form': patron_form, 'patron_type_form': patron_type_form}
		
	# if we have both:
	else:
		item = get_object_or_404(Item, pk=item_id)
		patron = get_object_or_404(Patron, pk=patron_id)
		context = {'item': item, 'patron': patron}
	
	return render(request, 'catalog/checkout.html', context)

def checkin(request):
	context = {}
	return render(request, 'catalog/checkin.html', context)

# helpers

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	
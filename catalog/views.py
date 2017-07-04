# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .forms import PatronSearchForm
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
	patron_query = request.GET.get('patron_query')	
	if (patron_query is not None):
		form = PatronSearchForm({'patron_query':patron_query})
		
		# run search query
		query_results = Patron.objects.filter(patron_name__icontains=patron_query)
		
		context = {'form': form, 'patron_query': patron_query, 'query_results': query_results}
	else:
		form = PatronSearchForm()
		context = {'form': form}

	return render(request, 'catalog/patron.html', context)
	
def patron_record(request, patron_id):
	patron = get_object_or_404(Patron, pk=patron_id)
	context = {'patron': patron}
	return render(request, 'catalog/patron_record.html', context)

	
	
	
	
	
	
	
	
	
	
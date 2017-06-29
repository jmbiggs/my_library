# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

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

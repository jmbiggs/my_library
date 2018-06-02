# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils import formats, timezone

from .forms import SearchModeForm, SearchForm, PatronForm, ItemForm, AuthorshipForm
from .models import Item, Patron, Author, CheckOut

from dal import autocomplete

class AuthorAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		qs = Author.objects.all()
		
		if self.q:
			qs = qs.filter(Q(author_name__icontains=self.q))
		
		return qs

def index(request):
	# get url parameters (depending on request type)
	if request.method == 'POST':
		search_mode = None
		query = None
		item_id = request.POST.get('item')
		patron_id = request.POST.get('patron')
		action = request.POST.get('action')
	else:	
		search_mode = request.GET.get('mode')
		query = request.GET.get('query')
		item_id = request.GET.get('item')
		patron_id = request.GET.get('patron')
	
	# get item and patron
	if item_id is not None:
		item = get_object_or_404(Item, pk=item_id)
	else:
		item = None		
	if patron_id is not None:
		patron = get_object_or_404(Patron, pk=patron_id)			
	else:
		patron = None
		
	checkout_object = None
	checkedin_item = None
	if request.method == 'POST':
		if action == 'checkin':
			checkin(item)
			checkedin_item = item
			item = None

		elif action == 'checkout':
			checkout_object = checkout(patron, item)
			if checkout_object is not None:
				# clear the item, but keep patron 'logged in'
				item = None
			
	# set up search mode form
	# - if user hasn't specified a choice, use item as default- unless an item has already been specified
	if search_mode is None:
		if item is not None:
			search_mode = 'patron'
		else:
			search_mode = 'item'
	mode_form = SearchModeForm({'mode': search_mode})

	# perform search if necessary
	if query is None:
		search_form = SearchForm()
		results = None
	else:
		search_form = SearchForm({'query': query})
		if search_mode == 'patron':
			results = patron_query(query)
		else:
			results = item_query(query)
		
	context = {'mode': search_mode, 'mode_form': mode_form, 'search_form': search_form, 'item': item, 'results': results, 'patron': patron, 'checkout_object': checkout_object, 'checkedin_item': checkedin_item}

	return render(request, 'catalog/index.html', context)

def new_item(request):
	authors_template='catalog/authors.html'
	
	if request.method == 'POST':
		author_form = AuthorshipForm(request.POST)
		form = ItemForm(request.POST)
		if author_form.is_valid() and not author_form.is_blank():
			author_form.save()
		if form.is_valid():		
			form.save()
			updated = True
		else:
			updated = False
	else:
		form = ItemForm()
		author_form = AuthorshipForm()
		updated = None
		
	context = {'form': form, 'author_form': author_form, 'updated': updated, 'authors_template': authors_template}
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

	# get patron's checkout records
	current_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=True)
	old_checkouts = CheckOut.objects.filter(patron=patron).filter(check_in_date__isnull=False)
	
	context = {'patron': patron, 'form': form, 'updated': updated, 'current_checkouts': current_checkouts, 'old_checkouts': old_checkouts}
	return render(request, 'catalog/patron_record.html', context)

# database functions

# checkout item to patron (changes database)
def checkout(patron, item):
	if patron is not None and item is not None:
		if item.is_checked_out():
			checkin(item)
		
		due_date = timezone.now()
		checkout_object = CheckOut(due_date=due_date, item=item, patron=patron)
		checkout_object.save()
		return checkout_object
	else:
		return None
		
# check item in (changes database)
def checkin(item):
	checkouts = CheckOut.objects.filter(item_id=item.id).filter(check_in_date__isnull=True)
	for checkout in checkouts:
		checkout.check_in_date = timezone.now()
		checkout.save()

# run a patron search on the database using given query
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

# run an item search on the database using given query	
def item_query(query):
	if query == '':
		return Item.objects.all()
	
	if is_int(query):
		id_query = Q(pk=query)
	else:
		id_query = Q()

	title_query = Q(title__icontains=query)
	author_query = Q(authors__author__author_name__icontains=query)			
	return Item.objects.filter(id_query | title_query | author_query).distinct()

# helpers

# returns whether given string can be parsed as an integer
def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False
	

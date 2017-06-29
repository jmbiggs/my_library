# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Item, Patron, Author, CheckOut

class ItemAdmin(admin.ModelAdmin):
	fields = ('media_type', 'title', 'authors', 'publication_date', 'catalog_id', 'shelf_location', 'isbn', 'upc', 'lost', 'condition', 'notes')

class PatronAdmin(admin.ModelAdmin):
	fields = ('patron_name', 'email')

class AuthorAdmin(admin.ModelAdmin):
	fields = ('author_name', 'author_type')

class CheckOutAdmin(admin.ModelAdmin):
	fields = ('patron', 'item', 'due_date')

admin.site.register(Item, ItemAdmin)
admin.site.register(Patron, PatronAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(CheckOut, CheckOutAdmin)
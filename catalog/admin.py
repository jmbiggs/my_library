# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Item, Patron, Author, CheckOut

admin.site.register(Item)
admin.site.register(Patron)
admin.site.register(Author)
admin.site.register(CheckOut)
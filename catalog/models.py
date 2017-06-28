# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Patron(models.Model):
	patron_name = models.CharField(max_length=50)
	email = models.EmailField()
	
	def __str__(self):
		return self.patron_name
	
class Author(models.Model):
	WRITER = 'writer'
	ILLUSTRATOR = 'illustrator'
	INTRODUCTION = 'introduction'
	TRANSLATOR = 'translator'
	AUTHOR_TYPE_CHOICES = (
		(WRITER, 'Writer'),
		(ILLUSTRATOR, 'Illustrator'),
		(TRANSLATOR, 'Translator'),
	)
	
	author_name = models.CharField(max_length=50)
	author_type = models.CharField(
		max_length=50,
		choices=AUTHOR_TYPE_CHOICES,
		default=WRITER,
	)
	
	def __str__(self):
		return self.author_name
	
class Item(models.Model):
	catalog_id = models.CharField(max_length=50)
	isbn = models.CharField(max_length=50, blank=True, null=True)
	upc = models.CharField(max_length=50, blank=True, null=True)
	condition = models.CharField(max_length=50, blank=True, null=True)
	media_type = models.CharField(max_length=50)
	aquisition_date = models.DateTimeField(auto_now_add=True)
	last_modified_date = models.DateTimeField(auto_now=True, null=True)
	notes = models.TextField(blank=True, null=True)
	title = models.CharField(max_length=50)
	authors = models.ManyToManyField(Author, blank=True)
	shelf_location = models.CharField(max_length=50, blank=True, null=True)
	publication_date = models.DateField(blank=True, null=True)
	api_link = models.CharField(max_length=150, blank=True, null=True)

	def __str__(self):
		return self.title + ' (' + self.media_type + ')'

class CheckOut(models.Model):
	check_in_date = models.DateTimeField(blank=True, null=True)
	check_out_date = models.DateTimeField(auto_now_add=True)
	due_date = models.DateTimeField()
	item = models.ForeignKey(Item)
	patron = models.ForeignKey(Patron)

	def __str__(self):
		return str(self.id) + ' (' + self.patron.patron_name + ') ' + self.item.title

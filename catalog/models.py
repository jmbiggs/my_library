# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Patron(models.Model):
	patron_name = models.CharField(max_length=50)
	email = models.EmailField()
	
	def __str__(self):
		return self.patron_name
	
class Author(models.Model):
	# group types
	BOOK = 'book'
	FILM = 'film'
	MUSIC = 'music'
	
	# book types
	AUTHOR = 'author'
	ILLUSTRATOR = 'illustrator'
	INTRODUCTION = 'introduction'
	TRANSLATOR = 'translator'
	
	# film types
	DIRECTOR = 'director'
	CAST = 'cast'
	WRITER = 'writer'
	EDITOR = 'editor'
	COMPOSER = 'composer'	
	
	# music types
	ARTIST = 'artist'
	
	# choice types
	AUTHOR_TYPE_CHOICES = (
		(BOOK, (
			(AUTHOR, 'Author'),
			(ILLUSTRATOR, 'Illustrator'),
			(INTRODUCTION, 'Introduction'),
			(TRANSLATOR, 'Translator'),
		)),
		(FILM, (
			(DIRECTOR, 'Director'),
			(WRITER, 'Writer'),
			(EDITOR, 'Editor'),
			(COMPOSER, 'Composer'),
		)),
		(MUSIC, (
			(ARTIST, 'Artist'),
		)),
	)
	
	author_name = models.CharField(max_length=50)
	author_type = models.CharField(
		max_length=50,
		choices=AUTHOR_TYPE_CHOICES,
		default=AUTHOR,
	)
	
	def __str__(self):
		return self.author_name + ' (' + self.author_type + ')'
	
class Item(models.Model):
	# media type groups
	BOOK = 'book'
	FILM = 'film'
	MUSIC = 'music'

	# book types
	HARDCOVER = 'hardcover'
	PAPERBACK = 'paperback'
	MAGAZINE = 'magazine'
	ZINE = 'zine'
	
	# film types
	DVD = 'dvd'
	BLURAY = 'bluray'
	VHS = 'vhs'
	LASERDISC = 'laserdisc'
	
	# music types
	RECORD = 'record'
	CD = 'cd'
	CDR = 'cdr'
	CASSETTE = 'cassette'
	USB = 'usb'
	
	# media types
	MEDIA_TYPE_CHOICES = (
		(BOOK, (
			(HARDCOVER, 'Hardcover'),
			(PAPERBACK, 'Paperback'),
			(MAGAZINE, 'Magazine'),
			(ZINE, 'Zine'),
		)),
		(FILM, (
			(DVD, 'DVD'),
			(BLURAY, 'Blu-Ray'),
			(VHS, 'VHS'),
			(LASERDISC, 'Laserdisc'),
		)),
		(MUSIC, (
			(RECORD, 'Vinyl Record'),
			(CD, 'CD'),
			(CDR, 'CD-R'),
			(CASSETTE, 'Cassette Tape'),
			(USB, 'USB Drive'),
		)),
	)
	
	media_type = models.CharField(
		max_length=50,
		choices=MEDIA_TYPE_CHOICES,
	)	
	catalog_id = models.CharField(max_length=50)
	isbn = models.CharField(max_length=13, blank=True, null=True)
	upc = models.CharField(max_length=12, blank=True, null=True)
	condition = models.CharField(max_length=50, blank=True, null=True)
	aquisition_date = models.DateTimeField(auto_now_add=True)
	last_modified_date = models.DateTimeField(auto_now=True, null=True)
	notes = models.TextField(blank=True, null=True)
	title = models.CharField(max_length=50)
	authors = models.ManyToManyField(Author, blank=True)
	shelf_location = models.CharField(max_length=50, blank=True, null=True)
	publication_date = models.DateField(blank=True, null=True)
	lost = models.BooleanField(default=False)
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

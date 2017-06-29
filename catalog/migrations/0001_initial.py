# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-27 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=50)),
                ('author_type', models.CharField(choices=[('writer', 'Writer'), ('illustrator', 'Illustrator'), ('translator', 'Translator')], default='writer', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catalog_id', models.CharField(max_length=50)),
                ('isbn', models.CharField(blank=True, max_length=50)),
                ('upc', models.CharField(blank=True, max_length=50)),
                ('condition', models.CharField(blank=True, max_length=50)),
                ('media_type', models.CharField(max_length=50)),
                ('aquisition_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('title', models.CharField(max_length=50)),
                ('shelf_location', models.CharField(blank=True, max_length=50)),
                ('publication_date', models.DateField(blank=True)),
                ('api_link', models.CharField(blank=True, max_length=150)),
                ('authors', models.ManyToManyField(blank=True, to='catalog.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Patron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patron_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-28 22:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
                ('author_type', models.CharField(choices=[('book', (('author', 'Author'), ('illustrator', 'Illustrator'), ('introduction', 'Introduction'), ('translator', 'Translator'))), ('film', (('director', 'Director'), ('writer', 'Writer'), ('editor', 'Editor'), ('composer', 'Composer'))), ('music', (('artist', 'Artist'),))], default='author', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateTimeField(blank=True, null=True)),
                ('check_out_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('book', (('hardcover', 'Hardcover'), ('paperback', 'Paperback'), ('magazine', 'Magazine'), ('zine', 'Zine'))), ('film', (('dvd', 'DVD'), ('bluray', 'Blu-Ray'), ('vhs', 'VHS'), ('laserdisc', 'Laserdisc'))), ('music', (('record', 'Vinyl Record'), ('cd', 'CD'), ('cdr', 'CD-R'), ('cassette', 'Cassette Tape'), ('usb', 'USB Drive')))], max_length=50)),
                ('catalog_id', models.CharField(max_length=50)),
                ('isbn', models.CharField(blank=True, max_length=13, null=True)),
                ('upc', models.CharField(blank=True, max_length=12, null=True)),
                ('condition', models.CharField(blank=True, max_length=50, null=True)),
                ('aquisition_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('title', models.CharField(max_length=50)),
                ('shelf_location', models.CharField(blank=True, max_length=50, null=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('lost', models.BooleanField(default=False)),
                ('api_link', models.CharField(blank=True, max_length=150, null=True)),
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
        migrations.AddField(
            model_name='checkout',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Item'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='patron',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Patron'),
        ),
    ]

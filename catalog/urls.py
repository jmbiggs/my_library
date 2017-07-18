from django.conf.urls import url

from . import views

urlpatterns = [
	# index
	url(r'^$', views.index, name='index'),
	
	# browse
	url(r'^browse/$', views.browse, name='browse'),
	
	# item record
	url(r'^item/(?P<item_id>[0-9]+)/$', views.item_record, name='item_record'),	
	
	# patron lookup
	url(r'^patron/$', views.patron_lookup, name='patron_lookup'),
	
	# patron record
	url(r'^patron/(?P<patron_id>[0-9]+)/$', views.patron_record, name='patron_record'),
	
	# check out
	url(r'^checkout/$', views.checkout, name='checkout'),
	
	# check in
	url(r'^checkin/$', views.checkin, name='checkin'),
]

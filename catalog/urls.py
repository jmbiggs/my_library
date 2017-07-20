from django.conf.urls import url

from . import views

urlpatterns = [
	# index
	url(r'^$', views.index, name='index'),
	
	# item record
	url(r'^item/(?P<item_id>[0-9]+)/$', views.item_record, name='item_record'),	

	# patron record
	url(r'^patron/(?P<patron_id>[0-9]+)/$', views.patron_record, name='patron_record'),
]

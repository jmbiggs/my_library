from django.conf.urls import url

from . import views

urlpatterns = [
	# index
	url(r'^$', views.index, name='index'),
	
	# browse
	url(r'^browse/$', views.browse, name='browse'),
	
	# item record
	url(r'^item/(?P<item_id>[0-9]+)/$', views.item_record, name='item_record'),	
]

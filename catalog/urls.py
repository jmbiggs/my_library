from django.conf.urls import url

from . import views
from .views import AuthorAutoComplete
from .models import Author

urlpatterns = [
	# index
	url(r'^$', views.index, name='index'),
	
	# new item record
	url(r'^authors.html$', views.new_item, name='new_item'),
	url(r'^item/$', views.new_item, name='new_item'),
		
	# item record
	url(r'^item/(?P<item_id>[0-9]+)/$', views.item_record, name='item_record'),	

	# new patron record
	url(r'^patron/$', views.new_patron, name='new_patron'),

	# patron record
	url(r'^patron/(?P<patron_id>[0-9]+)/$', views.patron_record, name='patron_record'),
	
	# author auto complete data
	url(r'^author-autocomplete/$', AuthorAutoComplete.as_view(create_field='author_name'), name='author-autocomplete'),
]

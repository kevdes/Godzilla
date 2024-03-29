from django.conf.urls import patterns, url
from management import views
from management import forms
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	# ex: /management/5/    
    url(r'^client/new/$', login_required(views.CreateClientView.as_view()), name='client-new'),
	url(r'^clients/$', login_required(views.ListClientView.as_view()), name='client-list'),
	url(r'^client/(?P<pk>\d+)/$', login_required(views.DetailClientView.as_view()), name='client-detail'),
	url(r'^client/edit/(?P<pk>\d+)/$', login_required(views.UpdateClientView.as_view()), name='client-edit'),
	url(r'^title/new/$', views.createTitle, name='title-new'),
	url(r'^title/new/(?P<client_id>\d+)/$', views.createTitleClient, name='title-new-client'),	
	url(r'^title/(?P<pk>\d+)/$', login_required(views.DetailTitleView.as_view()), name='title-detail'),	
	url(r'^title/edit/(?P<pk>\d+)/$', views.editTitle, name='title-edit'),
	url(r'^product/(?P<product_id>\d+)/$', views.product, name='product-detail'),
	url(r'^product/new/(?P<title_id>\d+)/$', views.createProduct, name='product-new'),
	url(r'^product/edit/(?P<product_id>\d+)/$', views.editProduct, name='product-edit'),
)



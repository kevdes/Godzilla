from django.conf.urls import patterns, url
from authoring import views
from authoring import forms

urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
	# ex: /management/5/    
	url(r'^product/(?P<product_id>\d+)/asset/new$', views.createAsset, name='asset-new'),
	url(r'^product/(?P<product_id>\d+)/asset/edit/(?P<asset_id>\d+)/$', views.editAsset, name='asset-edit'),
	url(r'^product/(?P<product_id>\d+)/asset/(?P<asset_id>\d+)/$', views.asset, name='asset-detail'),
	url(r'^product/(?P<product_id>\d+)/asset/(?P<asset_id>\d+)/report/new$', views.createReport, name='report-new'),
	url(r'^product/(?P<product_id>\d+)/asset/(?P<asset_id>\d+)/report/edit/(?P<report_id>\d+)$', views.editReport, name='report-edit'),
	url(r'^product/(?P<product_id>\d+)/asset/(?P<asset_id>\d+)/report/(?P<report_id>\d+)$', views.report, name='report-detail'),
	url(r'^testing/$', views.showUnsubmittedTesting, name='testing-submit'),
	url(r'^testing/(?P<days>\d+)/$', views.showUnsubmittedTesting, name='testing-submit'),
	url(r'^report/response/(?P<report_id>\d+)/$', views.reportResponse, name='report-response'),
)



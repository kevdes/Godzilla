from django.conf.urls import patterns, url
from testing import views
from testing import forms

urlpatterns = patterns('',
    url(r'^$', views.showTesting, name='testing-list'),
    url(r'^report/$', views.qaReport, name='qa'),    
	url(r'^report/(?P<report_id>\d+)/$', views.qaReport, name='testing-start'),
	url(r'^report/resume/(?P<report_id>\d+)/$', views.qaResume, name='testing-resume'),
	url(r'^report/submit/(?P<report_id>\d+)/$', views.qaSubmit, name='testing-submit'),
	url(r'^user/new/$', views.CreateCERUserView.as_view(), name='user-new'),
	url(r'^user/edit/$', views.UpdateCERUser, name='user-edit'),
	# ex: /management/5/    
)



from django.conf.urls import patterns, url
from materials import views

urlpatterns = patterns('',
    #url(r'^$', views.showTesting, name='testing-list'),
    url(r'^test/$', views.show_dir, name='show_dir'),
    url(r'^file/$', views.show_file, name='show_file'),
    url(r'^aspect/$', views.return_aspect, name='get_aspect'),
	# ex: /management/5/    
)



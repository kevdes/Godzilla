from django.conf.urls import patterns, include, url

from django.contrib import admin

from accounts import views

admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    url(r'^management/', include('management.urls')),
    url(r'^authoring/', include('authoring.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.loginPage, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),
)

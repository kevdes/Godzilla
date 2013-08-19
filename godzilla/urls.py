from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^management/', include('management.urls')),
    url(r'^authoring/', include('authoring.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

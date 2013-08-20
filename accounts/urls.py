from django.conf.urls import patterns, url
from accounts import views


urlpatterns = patterns('',
	url(r'^cer/$', views.loginCER, name='login-cer'),
)



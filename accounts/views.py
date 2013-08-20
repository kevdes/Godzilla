from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django import forms
from django.shortcuts import render 
from django.template import Context

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User, Group

@sensitive_post_parameters()
@csrf_protect
@never_cache
def loginPage(request, authentication_form=AuthenticationForm, *args, **kwargs):

	cer_users = User.objects.filter(groups__name='CER').exclude(groups__name='management').exclude(groups__name='authoring').exclude(groups__name='admin')

	if request.POST:
		form = authentication_form(request, data=request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			return HttpResponseRedirect(reverse('index'))
	else:
		form = authentication_form(request)
	context = {'page_title': 'Report', 'form': form, 'cer_users': cer_users}
	return render(request, 'accounts/login.html', context)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def loginCER(request):
	if request.POST and not request.POST.get("cer_login") == '':
		username = User.objects.get(id = request.POST.get("cer_login")).username
		new_user = authenticate(username=username, password='cer')  # password must be cer !!

		try:
			auth_login(request, new_user)
		except:
			return HttpResponseRedirect(reverse('login'))
		return HttpResponseRedirect(reverse('index'))
	else:
		return HttpResponseRedirect(reverse('login'))


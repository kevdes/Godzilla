from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django import forms
from django.shortcuts import render 
from django.template import Context





from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User, Group

from accounts.models import CentralUser




@sensitive_post_parameters()
@csrf_protect
@never_cache
def loginCER(request):
	if request.POST and not request.POST.get("cer_login") == '':
		username = CentralUser.objects.get(id = request.POST.get("cer_login")).username

		try:
			auth_login(request, new_user)
		except:
			return HttpResponseRedirect(reverse('login'))
		return HttpResponseRedirect(reverse('testing-list'))
	else:
		return HttpResponseRedirect(reverse('login'))


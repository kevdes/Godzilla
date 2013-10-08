from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_control

from datetime import datetime

from django.views.generic import CreateView
from django.views.generic import UpdateView

from testing.forms import ReportItemForm, ReportFormSet, ReportUserForm, CERUsers, CERUser

from authoring.models import AssetReport, AssetStatus, AssetReportStatus
from testing.models import ReportItem, CentralUser

from mail.send_mail import send_QA_report


# Create your views here.
def showTesting(request): 
	if request.method == 'POST':
		for item in request.POST:
			if '_test' in item:
				report_id = str(item).replace('_test', '')
				return HttpResponseRedirect(reverse('testing-start',  kwargs={'report_id': report_id}))
			elif '_resume' in item:
				report_id = str(item).replace('_resume', '')
				return HttpResponseRedirect(reverse('testing-resume', kwargs={'report_id': report_id}))
		

	qaRequestStatus = AssetReportStatus.objects.get(status='QA Request')
	qaPostponedStatus = AssetReportStatus.objects.get(status='QA Postponed')

	testing_list = AssetReport.objects.filter(status=qaRequestStatus, submitted=True, completed=False).order_by('date_created')
	progress_list = AssetReport.objects.filter(status=qaPostponedStatus).order_by('date_created')

	cer_user = CERUsers()

	context = {'testing_list': testing_list, 'progress_list':progress_list, 'title': 'QA requests', 'cer_user': cer_user }
	return render(request, 'testing/testing.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def qaReport(request, report_id): 	
	qaRequest = AssetReport.objects.get(id=report_id)
	if qaRequest.completed == True:
		report_id = AssetReport.objects.get(response_to=report_id).pk
		return HttpResponseRedirect(reverse('testing-resume', kwargs={'report_id': report_id}))
	return doQAReport(request, qaRequest)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def qaResume(request, report_id): 	
	qaReport = get_object_or_404(AssetReport, id=report_id)
	if qaReport.submitted == True:
		return HttpResponseRedirect(reverse('testing-list'))
	qaRequest = qaReport.response_to

	return doQAReport(request, qaRequest, qaReport)

def doQAReport(request, qaRequest, qaReport=None):

	form_errors = ""
	
	if qaReport:
		title = 'QA Report Continue'
		qaItems = ReportItem.objects.all().filter(asset_report=qaReport)
	else:
		title = 'QA Report'
		qaItems = None


	if request.method == 'POST':
		user_form = ReportUserForm(data=request.POST)
		
		formset = ReportFormSet(data=request.POST, instance=qaReport)

		#print formset.cleaned_data
		if user_form.is_valid():

			if formset.is_valid():

				for item in request.POST:
					if 'report_postpone' in item:
						reportStatus = AssetReportStatus.objects.get(status='QA Postponed')
						assetStatus = AssetStatus.objects.get(status='QA Postponed')
						isCompleted = False
						isSubmitted = False
						title = 'QA Saved'
					elif 'report_save' in item:
						reportStatus = AssetReportStatus.objects.get(status='QA Report')
						assetStatus = AssetStatus.objects.get(status='Attention Required')
						isCompleted = False  # this is used for responses
						isSubmitted = True
						title = 'QA Submitted'

				if str(request.user) == 'AnonymousUser':
					user = None
				else:					
					user = request.user

				if qaReport:
					qaReport.status = reportStatus
					#qaReport.contents = json_output
					qaReport.submitted = isSubmitted
					submitted_by = user
					qaReport.save()
				else:
					qaReport = AssetReport.objects.create(
						asset = qaRequest.asset,
						status = reportStatus,
						#contents = json_output,
						work_order = qaRequest.work_order,
						disc_number = qaRequest.disc_number,
						response_to = qaRequest,
						submitted = isSubmitted,				
						created_by = user,
						submitted_by = user
					)
					formset.instance = qaReport

	
				if formset.is_valid():
					formset.save(commit=False)
					for form in formset:											
						if not form.instance.pk:
							form.instance.cer_user = user_form.cleaned_data['user']
					formset.save()

#				for form in formset.cleaned_data:
#					if form:						
#						reportItem = ReportItem.objects.create(
#							asset_report = qaReport,
#							cer_user = user_form.cleaned_data['user'],
#							comment = form['comment'],
#							severity = form['severity'] )
#						reportItem.save()



				qaRequest.completed = True
				qaRequest.save()

				qaRequest.asset.status = assetStatus				
				qaRequest.asset.save()

				#if submitted:
				if isSubmitted:
					email_list = send_QA_report(qaReport.id)
				else:
					email_list = []
					#email_list = send_QA_report(qaReport.id)

				#return HttpResponseRedirect("%s?submit=%s" % (reverse('testing-submit', kwargs={'report_id': qaReport.id}), isSubmitted))

				context = {'title': title, 'email_list': email_list, 'isSubmitted': isSubmitted}
				return render(request, 'testing/report_submit.html', context)

	else:
		user_form = ReportUserForm()
		formset = ReportFormSet(instance=qaReport)
	#qaReportItem = qareport

	context = {'title': title, 'qaRequest': qaRequest, 'formset': formset, 'user_form': user_form, 'qaItems': qaItems, 'form_errors': form_errors}
	return render(request, 'testing/report.html', context)


def qaSubmit(request, report_id):

	if request.GET.get('submit') == 'True':
		title = 'QA Submitted'
	elif request.GET.get('submit') == 'False':
		title = 'QA Saved'
	else:
		title = 'Error'

	context = {'title': title }
	return render(request, 'testing/report_submit.html', context)


class CreateCERUserView(CreateView):
	model = CentralUser

	def get_success_url(self):
		return reverse('testing-list')

	def get_context_data(self, **kwargs):

		context = super(CreateCERUserView, self).get_context_data(**kwargs)
		context['action'] = reverse('user-new')
		return context

def UpdateCERUser(request):

	returnPage = reverse('testing-list')

	if request.GET.get('user'):
		user_id = request.GET['user']

	CER_User = get_object_or_404(CentralUser, pk=user_id)

	if request.method == 'POST':

		form = CERUser(request.POST, instance=CER_User)
		if form.is_valid():
			CER_User = form.save()
			return HttpResponseRedirect(reverse('testing-list'))
	else:        
		form = CERUser(instance=CER_User)

	context = {'title': 'Edit Central User', 'form': form, 'instance': CER_User, 'returnPage': returnPage}
	return render(request, 'testing/centraluser_form.html', context)



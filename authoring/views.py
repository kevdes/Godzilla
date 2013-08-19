# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import DetailView

from authoring.forms import AssetForm, AssetFormSet, EditAssetForm, CreateAssetReportForm, CreateBareAssetReportForm

from management.models import Product
from authoring.models import Asset, AssetStatus, AssetType, AssetReport, AssetReportStatus


# Create your views here.
def createAsset(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	if request.method == 'POST':
		formset = AssetFormSet(data=request.POST)
		if formset.is_valid():
			for form in formset.cleaned_data:
				if form:
					if form['name'] == "" :
						theName = form['asset_type'].name
					else:
						theName = form['name']
					asset = Asset.objects.create(
						name = theName,
						asset_type = form['asset_type'],
						status = AssetStatus.objects.get(status='New'),  
						product = product )
					asset.save()
			return HttpResponseRedirect(reverse('product-detail', kwargs={'product_id': product.id}))

	else:
		formset = AssetFormSet()
	context = {'page_title': 'Create Assets', 'instance': product, 'formset': formset }
	return render(request, 'authoring/asset_formset.html', context)


def editAsset(request, product_id, asset_id):
	asset = get_object_or_404(Asset, pk=asset_id)
	if request.method == 'POST':
		form = EditAssetForm(request.POST, instance=asset)
		if form.is_valid():
			# create a new item
			asset = form.save(commit=False)
			name = form.cleaned_data['name']
			asset_type = asset.asset_type
			status = asset.status
			product = asset.product
			asset.save()
			# Always redirect after a POST
			return HttpResponseRedirect(reverse('asset-detail', kwargs={'product_id': product_id, 'asset_id': asset.id}))
	else:        
		form = EditAssetForm(instance=asset)
	context = {'page_title': 'Edit Asset', 'title': asset.name, 'form': form, 'instance': asset}
	return render(request, 'authoring/asset_form.html', context)

def asset(request, product_id, asset_id):  #product_id redundant?
	asset = get_object_or_404(Asset, pk=asset_id)
	return render(request, 'authoring/asset.html', {'asset': asset})

def createReport(request, product_id, asset_id):
	asset = get_object_or_404(Asset, pk=asset_id)
	discNumber = ''
	reportStatus = ''

	if request.GET.get('type'):
		reportType = request.GET['type']		
	else:
		reportType = 'test'	

	if reportType == 'test':
		reportStatus = AssetReportStatus.objects.get(status='QA Request')

		if request.method == 'POST':
			form = CreateAssetReportForm(request.POST)
			if form.is_valid():
				# create a new item
				try: 
					discNumber = AssetReport.objects.latest('disc_number').disc_number + 1
				except Exception:
					discNumber = 1

				assetReport = AssetReport.objects.create(
					asset = asset,
					status = reportStatus,				
					contents = form.cleaned_data['contents'],
					work_order = form.cleaned_data['work_order'],
					disc_number = discNumber,
					#response_to = form.cleaned_data['response_to'],
					submitted = form.cleaned_data['submitted']
				)
				asset.status = AssetStatus.objects.get(status='In Progress')
				asset.save()
			# Always redirect after a POST
			return HttpResponseRedirect(reverse('asset-detail', kwargs={'product_id': asset.product.id, 'asset_id': asset.id}))
		else:        
			form = CreateAssetReportForm(initial={'product': asset.product_id, 'asset_type': asset.asset_type, 'status': reportStatus})
			#form.initial['asset'] = asset.pk

	elif reportType == 'comment':
		reportStatus = AssetReportStatus.objects.get(status='Comment')

		if request.method == 'POST':
			form = CreateBareAssetReportForm(request.POST)
			if form.is_valid():
				# create a new item
				try: 
					discNumber = AssetReport.objects.latest('disc_number').disc_number + 1
				except Exception:
					discNumber = 1

				assetReport = AssetReport.objects.create(
					asset = asset,
					status = reportStatus,				
					contents = form.cleaned_data['contents'],
					#work_order = form.cleaned_data['work_order'],
					#disc_number = discNumber,
					#response_to = form.cleaned_data['response_to'],
					completed = True,
					submitted = True,
				)
			# Always redirect after a POST
			return HttpResponseRedirect(reverse('asset-detail', kwargs={'product_id': asset.product.id, 'asset_id': asset.id}))
		else:        
			form = CreateBareAssetReportForm(initial={'product': asset.product_id, 'asset_type': asset.asset_type, 'status': reportStatus})
			#form.initial['asset'] = asset.pk
	

	context = {'page_title': 'Report', 'form': form, 'instance': asset}
	return render(request, 'authoring/report_form.html', context)

def editReport(request, product_id, asset_id, report_id):
	assetReport = get_object_or_404(AssetReport, pk=report_id)
	if request.method == 'POST':
		form = CreateAssetReportForm(request.POST, instance=assetReport)
		if form.is_valid():
			# create a new item
			assetReport = form.save(commit=False)			
			contents = form.cleaned_data['contents'],
			work_order = form.cleaned_data['work_order'],
			#response_to = form.cleaned_data['response_to'],
			submitted = form.cleaned_data['submitted']
			assetReport.save()
			# Always redirect after a POST
			return HttpResponseRedirect(reverse('asset-detail', kwargs={'product_id': assetReport.asset.product.id, 'asset_id': assetReport.asset.id}))
	else:        
		form = CreateAssetReportForm(instance=assetReport)
	context = {'page_title': 'Edit Asset Report', 'title': assetReport.asset.product_id, 'form': form, 'instance': assetReport.asset}
	return render(request, 'authoring/report_form.html', context)

def report(request, product_id, asset_id, report_id):  #product_id redundant?
	assetReport = get_object_or_404(AssetReport, pk=report_id)
	return render(request, 'authoring/report_detail.html', {'assetreport': assetReport})	
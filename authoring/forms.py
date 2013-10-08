from django import forms
from django.forms.models import BaseFormSet, formset_factory, inlineformset_factory

from management.models import Product
from authoring.models import Asset, AssetReportStatus, AssetReport, ReportItemResponse
from testing.models import ReportItem

class AssetForm(forms.ModelForm):

	class Meta:
		model = Asset
		exclude = ['product', 'status']
 
	def __init__(self, *args, **kwargs):
		super(AssetForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = ['asset_type', 'name', ]
		#self.fields['status'].initial = '1'
		#self.fields['status'].widget.attrs['disabled'] = True

class BaseAssetFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):     
			super(BaseAssetFormSet, self).__init__(*args, **kwargs)
			#for form in self.forms:
			#	form.empty_permitted = False

		def _construct_form(self, index, **kwargs):
			return super(BaseAssetFormSet, self)._construct_form(index, **kwargs)

class EditAssetForm(forms.ModelForm):

	class Meta:
		model = Asset
		exclude = ['product', 'status', 'asset_type']
 
	def __init__(self, *args, **kwargs):
		super(EditAssetForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = ['name', ]
		

AssetFormSet = formset_factory(AssetForm, formset=BaseAssetFormSet)

class CreateAssetReportForm(forms.ModelForm):

	class Meta:
		model = AssetReport
		exclude = ['asset', 'response_to', 'status', 'disc_number', 'completed', 'created_by', 'submitted_by']

	def __init__(self, *args, **kwargs):
		super(CreateAssetReportForm, self).__init__(*args, **kwargs)
		self.fields['contents'].widget.attrs.update({'class' : 'span5'})
		#self.fields['work_order'].widget.attrs.update({'class' : 'control-label'})
		self.fields['submitted'].widget.attrs.update({'class' : 'checkbox'})

		#self.fields['asset'].queryset = Asset.objects.filter(product=self.initial['product'])
		#if self.initial:
		#	self.fields['status'].queryset = AssetReportStatus.objects.filter(asset_type=self.initial['asset_type']).order_by('display_order',)
		#	self.fields['status'].widget.attrs['disabled'] = True


class CreateBareAssetReportForm(forms.ModelForm):

	class Meta:
		model = AssetReport
		exclude = ['asset', 'response_to', 'status', 'disc_number', 'completed', 'work_order', 'submitted', 'created_by', 'submitted_by']

	def __init__(self, *args, **kwargs):		
		super(CreateBareAssetReportForm, self).__init__(*args, **kwargs)
		self.fields['contents'].widget.attrs.update({'class' : 'span5'})



class showTesting(forms.ModelForm):
	class Meta:
		model = AssetReport


class ReportResponseForm(forms.ModelForm):

	class Meta:
		model = ReportItemResponse
		exclude = ['user_created', ]

	"""
	def __init__(self, *args, **kwargs):
		report_id = kwargs.pop('report_id')
		super(ReportResponseForm, self).__init__(*args, **kwargs)
		self.prefix = report_id
	"""


ReportResponseFormset = inlineformset_factory(ReportItem, ReportItemResponse, ReportResponseForm, can_delete=False, extra=1, max_num=10)
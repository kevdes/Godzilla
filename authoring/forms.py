from django import forms
from django.forms.models import BaseFormSet, formset_factory


from management.models import Product
from authoring.models import Asset, AssetReportStatus, AssetReport

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
		exclude = ['asset', 'response_to', 'status', 'disc_number', 'completed']

	def __init__(self, *args, **kwargs):
		super(CreateAssetReportForm, self).__init__(*args, **kwargs)


		#self.fields['asset'].queryset = Asset.objects.filter(product=self.initial['product'])
		#if self.initial:
		#	self.fields['status'].queryset = AssetReportStatus.objects.filter(asset_type=self.initial['asset_type']).order_by('display_order',)
		#	self.fields['status'].widget.attrs['disabled'] = True


class CreateBareAssetReportForm(forms.ModelForm):

	class Meta:
		model = AssetReport
		exclude = ['asset', 'response_to', 'status', 'disc_number', 'completed', 'work_order', 'submitted']


class showTesting(forms.ModelForm):
	class Meta:
		model = AssetReport
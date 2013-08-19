from django import forms
from django.contrib.admin import widgets      

from management.models import Product
from management.models import Client
from management.models import Title


class CreateTitleForm(forms.ModelForm):
	class Meta:
		model = Title

class CreateClientTitleForm(forms.ModelForm):
	class Meta:
		model = Title
		exclude = ['client']

class CreateProductForm(forms.ModelForm):
	# requires a title to be created


	class Meta:
		model = Product
		exclude = ['title', ]

	def __init__(self, *args, **kwargs):
		super(CreateProductForm, self).__init__(*args, **kwargs)
		self.fields['due_date'].widget = widgets.AdminDateWidget()


class EditProductForm(forms.ModelForm):
	# requires a title to be created


	class Meta:
		model = Product
		exclude = ['title', 'product_type', ]

	def __init__(self, *args, **kwargs):
		super(EditProductForm, self).__init__(*args, **kwargs)
		self.fields['due_date'].widget = widgets.AdminDateWidget()

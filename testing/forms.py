from django import forms
from django.forms.models import BaseFormSet, formset_factory, inlineformset_factory, BaseInlineFormSet
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from django.db.models.query import EmptyQuerySet

from testing.models import CentralUser
from testing.models import ReportItem
from authoring.models import AssetReport, ReportItemResponse

from authoring.forms import ReportResponseFormset, ReportResponseForm

class ChoiceLabelWidget(forms.Widget):
	def render(self, name, value, attrs):
		final_attrs = self.build_attrs(attrs, name=name)
		return mark_safe(dict(self.choices)[int(value)]) + mark_safe("<input type='hidden' name='%s' value='%s' />" % (name, value))
		
	def _has_changed(self, initial, data):
		return False

class LabelWidget(forms.Widget):
	def render(self, name, value, attrs):
		final_attrs = self.build_attrs(attrs, name=name)
		return mark_safe(value) + mark_safe("<input type='hidden' name='%s' value='%s' />" % (name, value))
		
	def _has_changed(self, initial, data):
		return False


class ReportItemForm(forms.ModelForm):

	class Meta:
		model = ReportItem
		exclude = ['cer_user', 'response_comment', 'response_user', 'response_status', 'response_date' ]
			#comment = forms.CharField( widget=forms.Textarea(attrs={'cols': 80, 'rows': 6}), required=False )
	
	def __init__(self, *args, **kwargs):
		super(ReportItemForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['comment'].widget.attrs['cols'] = 80
		self.fields['comment'].widget.attrs['rows'] = 6


ReportFormSet = inlineformset_factory(AssetReport, ReportItem, ReportItemForm, can_delete=False, extra=3)

class ReportUserForm(forms.Form):
	cer_users = CentralUser.objects.filter(active=True)
	user = forms.ModelChoiceField(cer_users, label='Select user', empty_label='-----------', required=True)


class BaseReportItemFormset(BaseInlineFormSet):
	def get_queryset(self):
		## See get_queryset method of django.forms.models.BaseModelFormSet
		if not hasattr(self, '_queryset'):
			self._queryset = self.queryset.filter(response_comment=u'')
		return self._queryset


class CERUsers(forms.Form):
	cer_users = CentralUser.objects.all()
	user = forms.ModelChoiceField(cer_users, label='Edit CER user:', empty_label=None, required=True)


class CERUser(forms.ModelForm):

	class Meta:
		model = CentralUser


class ReportResponseForm(forms.ModelForm):

	class Meta:
		model = ReportItem
		exclude = ['cer_user', 'comment', 'severity', 'response_user', 'response_date' ]
		widgets = { 
			'cer_user': ChoiceLabelWidget(),
			'severity': ChoiceLabelWidget(),
			'comment': LabelWidget(),
			'date_created': LabelWidget(),
		}
	
	def __init__(self, *args, **kwargs):
		super(ReportResponseForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['response_comment'].widget.attrs['cols'] = 70
		self.fields['response_comment'].widget.attrs['rows'] = 6


ReportItemFormset = inlineformset_factory(AssetReport, ReportItem, form=ReportResponseForm, can_delete=False, extra=0)
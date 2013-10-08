from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from management.models import Product
from testing.models import ReportItem



# Create your models here.
class AssetStatus(models.Model):
	status = models.CharField('status name', max_length=50)
	color = models.CharField('hex color', max_length=20, blank=True)
	finalised = models.BooleanField('mark asset as complete', default=False)
	display_order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.status

	class Meta:
		verbose_name_plural = 'asset status'


class AssetType(models.Model):
	name = models.CharField(max_length=50)
	display_order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ('display_order', )


class Asset(models.Model):
	name = models.CharField(max_length=50, blank=True)
	asset_type = models.ForeignKey(AssetType)
	status = models.ForeignKey(AssetStatus)
	product = models.ForeignKey(Product)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def awaitingQA(self):
		if not (str(self.status) == 'Awaiting QA' or str(self.status) == 'QA Submission Pending' \
		or str(self.status) == 'QA Postponed' or str(self.status) == 'Attention Required' or str(self.status) == 'Author Approved'):
			return False
		else:
			return True

	def getParentReports(self):
		return AssetReport.objects.filter(asset=self, response_to=None)

	def get_absolute_url(self):    	
		return reverse('asset-detail', kwargs={'asset_id': self.id, 'product_id': self.product.id})

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('date_created', 'date_updated')

class AssetReportStatus(models.Model):

	REPORT_TYPE_CHOICES = (
		('REQUEST', 'Request'),
		('REPORT', 'Report'),
		('APPROVAL', 'Approval'),
	)

	status = models.CharField('status name', max_length=50)
	color = models.CharField('hex color', max_length=20, blank=True)
	finalised = models.BooleanField('mark report as complete', default=False)
	display_order = models.IntegerField(default=1)
	#asset_type = models.ForeignKey(AssetType)
	report_type = models.CharField(max_length=50,
									  choices=REPORT_TYPE_CHOICES)

	def __unicode__(self):
		return self.status

	class Meta:
		verbose_name_plural = 'asset report status'


class AssetReport(models.Model):
	asset = models.ForeignKey(Asset)  #, limit_choices_to = {'product': 17})
	status = models.ForeignKey(AssetReportStatus)	
	contents = models.TextField('notes', blank=True)
	work_order = models.CharField('work order number', max_length=50, blank=True)
	disc_number = models.IntegerField('qa disc number', blank=True, null=True)
	response_to = models.ForeignKey('AssetReport', blank=True, null=True)
	submitted = models.BooleanField('submit for testing', default=False)
	completed = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User, related_name='creator', null=True)
	submitted_by = models.ForeignKey(User, related_name='submitter', null=True)

	def isEditable(self):
		if str(self.status) == 'QA Request' and not self.submitted:
			return True
		else:
			return False

	def getSubmittedText(self):
		if str(self.status) == 'QA Request':			
			if self.submitted:
				if str(self.work_order) == '':
					return 'Work order required'
				else:
					return ''
			else:
				return 'Not submitted'
		else:
			return ''

	def isQARequest(self):
		if str(self.status) == 'QA Request':
			return True
		else:
			return False

	def isQAReport(self):

		if str(self.status) == 'QA Report' or str(self.status) == 'QA Postponed':
			return True
		else:
			return False
	
	def getReportStatus(self):
		status = 'Author Approved'

		if self.submitted:
			for assetReportItem in self.reportitem_set.all():
				if assetReportItem.response_status == None:
					status = 'Response required'
					break
				elif str(assetReportItem.response_status) == 'Fixed - retest required' or str(assetReportItem.response_status) == 'To be fixed':
					status = 'Asset Rejected'  #Follow-up required
					break
		else:
			status = 'QA not complete'
		return status

	def getReportCSS(self):
		status_class = 'neutral'

		if self.submitted:
			for assetReportItem in self.reportitem_set.all():
				if assetReportItem.response_status == None:
					status_class = 'attention'
					break
				elif str(assetReportItem.response_status) == 'Fixed - retest required' or str(assetReportItem.response_status) == 'To be fixed':
					status_class = 'progress'
					break
				elif str(assetReportItem.response_status) == 'Acceptable':
					status_class = 'success'
		return status_class


	def reportItems(self):
		return ReportItem.objects.filter(asset_report=self).order_by('date_created')

	def getChildren(self):
		return AssetReport.objects.filter(response_to=self).order_by('date_created')

	def _get_full_submitted_by(self):
		return u'%s %s' % (self.submitted_by.first_name, self.submitted_by.last_name)

	def _get_full_created_by(self):
		return u'%s %s' % (self.created_by.first_name, self.created_by.last_name)

	full_submitted_by = property(_get_full_submitted_by)
	full_created_by = property(_get_full_created_by)

	def __unicode__(self):
		return u'%s > %s > %s' % (self.asset.product.full_name, self.asset, self.status)

	class Meta:
		ordering = ('date_created', 'date_updated')
		verbose_name_plural = 'asset report'
		get_latest_by = 'date_updated'


class ReportResponseStatus(models.Model):
	name = models.CharField('status name', max_length=50)
	color = models.CharField('class color', max_length=20, blank=True)
	display_order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name


class ReportItemResponse(models.Model):
	report_item = models.ForeignKey(ReportItem)
	comment = models.TextField()
	status = models.ForeignKey(ReportResponseStatus)
	user_created = models.ForeignKey(User)
	date_created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.comment
	

class ActionButton(models.Model):
	name = models.CharField(max_length=50)
	color = models.CharField('css class', max_length=20, blank=True)
	action = models.CharField(max_length=50, blank=True)
	status = models.ManyToManyField(AssetReportStatus)
	next_asset_status = models.ForeignKey(AssetStatus)
	display_order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name
		#return HTML code??

	class Meta:
		ordering = ('display_order', )
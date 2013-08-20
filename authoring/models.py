from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from management.models import Product

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

	def get_absolute_url(self):    	
		return reverse('asset-detail', kwargs={'asset_id': self.id, 'product_id': self.product.id})

	def __unicode__(self):
		return self.name

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

	def isEditable(self):
		if self.submitted:
			return False
		else:
			return True

	def getSubmittedText(self):
		if str(self.status) == 'QA Request':			
			if self.submitted:
				return 'Awaiting QA'
				#  unused: 
				if str(self.work_order) == '':
					return 'Work order required'
				else:
					return 'Awaiting QA'
			else:
				return 'Not submitted'
		else:
			return ''

	def isQA(self):
		if str(self.status) == 'QA Request' or str(self.status) == 'QA Report':
			return True
		else:
			return False

	def __unicode__(self):
		return u'%s > %s > %s' % (self.asset.product.full_name, self.asset, self.status)

	class Meta:
		ordering = ('date_created', )
		verbose_name_plural = 'asset report'
from django.db import models
from django.contrib.auth.models import User


class CentralUser(models.Model):
	username = models.CharField(max_length=50, unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		ordering = ('first_name', 'last_name')


class ReportItemSeverity(models.Model):
	name = models.CharField('status name', max_length=50)
	color = models.CharField('class color', max_length=20, blank=True)
	display_order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('display_order', )
		verbose_name_plural = 'report item severity'

class ReportResponseStatus(models.Model):
	name = models.CharField('status name', max_length=50)
	color = models.CharField('class color', max_length=20, blank=True)
	display_order = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name

class ReportItem(models.Model):
	asset_report = models.ForeignKey('authoring.AssetReport')
	cer_user = models.ForeignKey(CentralUser)
	comment = models.TextField()
	severity = models.ForeignKey(ReportItemSeverity)
	date_created = models.DateTimeField(auto_now_add=True)
	response_comment =  models.TextField(blank=True)
	response_user = models.ForeignKey(User, blank=True, null=True) 
	response_status = models.ForeignKey(ReportResponseStatus, blank=True, null=True)
	response_date = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True, null=True)

	class Meta:
		ordering = ('date_created', )
		
	def __unicode__(self):
		return self.comment
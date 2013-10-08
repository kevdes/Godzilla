from django.contrib import admin
from testing.models import CentralUser
from testing.models import ReportItem
from testing.models import ReportItemSeverity
from testing.models import ReportResponseStatus

class CentralUserAdmin(admin.ModelAdmin):
	list_display = ('username','first_name', 'last_name', 'active',)
	#search_fields = ['title']

class ReportItemAdmin(admin.ModelAdmin):
	list_display = ('asset_report', 'cer_user', 'comment', 'severity', 'date_created', 'response_comment', 'response_user', 'response_status', 'response_date', )



admin.site.register(CentralUser, CentralUserAdmin)
admin.site.register(ReportItem, ReportItemAdmin)
admin.site.register(ReportItemSeverity)
admin.site.register(ReportResponseStatus)

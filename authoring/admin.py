from django.contrib import admin

from authoring.models import AssetStatus
from authoring.models import AssetType
from authoring.models import Asset
from authoring.models import AssetReport
from authoring.models import AssetReportStatus
from authoring.models import ActionButton


class AssetTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'display_order')
	ordering = ('display_order', )


class AssetStatusAdmin(admin.ModelAdmin):
	list_display = ('status', 'display_order', 'color', 'finalised')
	ordering = ('display_order', )

class AssetAdmin(admin.ModelAdmin):
	list_display = ('product', 'asset_type', 'name', 'status')
	ordering = ('product', 'asset_type', 'date_created')

class AssetReporStatusAdmin(admin.ModelAdmin):
	list_display = ('status', 'report_type', 'display_order', 'color', 'finalised')
	ordering = ('report_type', 'display_order', )

class AssetReportAdmin(admin.ModelAdmin):
	list_display = ('asset', 'status', 'disc_number', 'submitted', 'completed', 'date_created', 'date_updated',)
	ordering = ('status', )


admin.site.register(AssetStatus, AssetStatusAdmin)
admin.site.register(AssetType, AssetTypeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetReport, AssetReportAdmin)
admin.site.register(AssetReportStatus, AssetReporStatusAdmin)
admin.site.register(ActionButton)

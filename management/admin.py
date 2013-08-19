from django.contrib import admin
from management.models import Client
from management.models import Title
from management.models import ProductStatus
from management.models import Product
from management.models import ProductType

from authoring.models import Asset

class ProductInline(admin.TabularInline):	
	model = Product
	extra = 0

	#readonly_fields = ('product',)

class AssetInline(admin.TabularInline):	
	model = Asset
	extra = 3

	fields = ('product', 'asset_type', 'name', 'status')
	ordering = ('asset_type', 'date_created')

	#readonly_fields = ('product',)

class TitleAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','client',)
	list_filter = ['client']
	#search_fields = ['title']

	inlines = [ProductInline]

class ProductAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','due_date','status',)
	list_filter = ['product_type','status', 'due_date']
	#search_fields = ['title']
	date_hierarchy = 'due_date'

	inlines = [AssetInline]

class ProductStatusAdmin(admin.ModelAdmin):
	list_display = ('status', 'display_order', 'color', 'finalised')
	ordering = ('display_order', )


admin.site.register(Client)
admin.site.register(Title, TitleAdmin)
admin.site.register(ProductStatus, ProductStatusAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)

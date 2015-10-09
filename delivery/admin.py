from django.contrib import admin

# Register your models here.
from .models import *

class FamilyAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)
    list_display = ('name', 'count_users')

class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_product_name', 'ref_user')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('producer', 'name', 'unit_price')

class DeliveryDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'comment', 'count_users')
    ordering = ('date',)
    list_filter = ('date',)

class ContractAdmin(admin.ModelAdmin):
    fields = ('producer', 'name', 'dates')
    filter_horizontal = ('dates',)
    list_display = ('producer', 'name', 'date_min', 'date_max', 'count_dates')
    list_filter = ('producer', 'date_min', )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('family', 'product', 'date', 'quantity')

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('family', 'contract', 'status', 'amount')
    list_filter = ('family','contract', 'status')

admin.site.register(Family, FamilyAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(DeliveryDate,DeliveryDateAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Order, OrderAdmin)

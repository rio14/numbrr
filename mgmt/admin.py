from django.contrib import admin

from .models import *
class Customer_admin(admin.ModelAdmin):
    list_display = ('name','owner','area')
class Staff_admin(admin.ModelAdmin):
    list_display = ('name','owner')
admin.site.register(Customer,Customer_admin)
admin.site.register(Staff,Staff_admin)

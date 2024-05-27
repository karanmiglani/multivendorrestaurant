from django.contrib import admin
from .models import Vendor
# Register your models here.

class CustomVendorAdmin(admin.ModelAdmin):
    list_display = ('user_profile' , 'vendor_name' ,'is_approved' ,'created_at')


admin.site.register(Vendor , CustomVendorAdmin)
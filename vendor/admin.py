from django.contrib import admin
from .models import Vendor , OpeningHours
# Register your models here.

class CustomVendorAdmin(admin.ModelAdmin):
    list_display = ('user_profile' , 'vendor_name' ,'is_approved' ,'created_at')
    list_editable = ('is_approved',)



class CustomOpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor' , 'day' , 'from_hours' , 'to_hours')

admin.site.register(Vendor , CustomVendorAdmin)
admin.site.register(OpeningHours , CustomOpeningHourAdmin)
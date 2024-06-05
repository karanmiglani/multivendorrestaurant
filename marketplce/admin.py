from django.contrib import admin
from .models import Cart , Tax
# Register your models here.


class CustomCartAdmin(admin.ModelAdmin):
    list_display = ('user' , 'product' , 'qty' , 'updated_at')



class CustomTaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type' , 'tax_percentage' , 'is_active')

admin.site.register(Cart , CustomCartAdmin)
admin.site.register(Tax , CustomTaxAdmin)



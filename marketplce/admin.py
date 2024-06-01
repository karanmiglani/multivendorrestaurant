from django.contrib import admin
from .models import Cart
# Register your models here.


class CustomCartAdmin(admin.ModelAdmin):
    list_display = ('user' , 'product' , 'qty' , 'updated_at')

admin.site.register(Cart , CustomCartAdmin)



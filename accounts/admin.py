from django.contrib import admin
from .models import User , UserProfile
from django.contrib.auth.admin import UserAdmin 

# Register your models here.

class CustomUserAdmin(UserAdmin):
    ordering = ['email']
    list_display = ("email", "first_name", "last_name","username", "is_active","role")
    ordering = ("-date_joined",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()








    
admin.site.register(User ,  CustomUserAdmin)
admin.site.register(UserProfile)
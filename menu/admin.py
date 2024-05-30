from django.contrib import admin
from .models import Category , Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name' , 'vendor' ,'created_at' ,'updated_at')
    search_fields = ('category_name' , 'vendor__vendor_name')
    prepopulated_fields = {'slug' :('category_name' , )}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('product_title' ,)}
    list_display = ('product_title' ,'price' ,'category' , 'vendor' ,  'created_at' ,'updated_at')
    search_fields = ('product_title' , 'category__category_name' ,'price' ,'vendor__vendor_name')
admin.site.register(Category , CategoryAdmin)
admin.site.register(Product , ProductAdmin)
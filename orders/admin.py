from django.contrib import admin
from .models import Payment , OrderModel , OrderedFood
# Register your models here.
admin.site.register(Payment)
admin.site.register(OrderModel)
admin.site.register(OrderedFood)

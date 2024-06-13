from django.contrib import admin
from .models import Payment , OrderModel , OrderedFood
# Register your models here.


class OrderFoodAdmin(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order' , 'payment' , 'user' , 'foodItem' , 'qty' , 'price' , 'amount')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number' , 'name' , 'phone' ,'email' , 'total' , 'payment_method' , 'order_status', 'order_placed_to','is_ordered' )
    inlines = [OrderFoodAdmin]


admin.site.register(Payment)
admin.site.register(OrderModel , OrderAdmin)
admin.site.register(OrderedFood)

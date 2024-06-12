from django.urls import path,include
from accounts.views import customerDashboard
from . import views

urlpatterns = [
    path('',customerDashboard , name = 'customer-dashboard'),
    path('profile'  , views.customerProfile , name='customer-profile'),
    path('my-orders'  , views.myOrders , name='my-orders'),
    path('order-details/<order_number>'  , views.orderDetails , name='order-details'),
]
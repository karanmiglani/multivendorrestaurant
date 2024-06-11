from django.urls import path,include
from accounts.views import customerDashboard
from . import views

urlpatterns = [
    path('',customerDashboard , name = 'customer-dashboard'),
    path('profile'  , views.customerProfile , name='customer-profile')
]
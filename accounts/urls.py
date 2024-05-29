from django.urls import path
from . import views


urlpatterns = [
    path('',views.myAccount),
    path('register-user/',views.registerUser , name = 'register-user'),
    path('register-vendor/',views.registerVendor , name = 'register-vendor'),
    path('login/' , views.login , name = 'login'),
    path('logout/' , views.logout , name='logout'),
    path('forgot-password/',views.forgotPassword, name = 'forgot-password'),
    path('reset-password-validate/<uidb64>/<token>/',views.resetPasswordValidate, name = 'reset-password-validate'),
    path('reset-password/',views.resetPassword, name = 'reset-password'),
    path('myAccount/' , views.myAccount , name = 'myAccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('activate/<uidb64>/<token>/',views.activate , name = 'activate')
]
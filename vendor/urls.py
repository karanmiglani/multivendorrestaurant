from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('',AccountViews.vendorDashboard , name = 'vendorDashboard' ),
    path('profile/' , views.profile , name = 'vendor-profile'),
    path('menu-builder/' , views.menuBuilder , name = 'menu-builder'),
    path('menu-builder/category/<int:pk>/' , views.foodItemsByCategory , name = 'food-items-by-category'),
    path('menu-builder/category/add/' , views.addCategory , name='add-category'),
    path('menu-builder/category/edit/<int:pk>' , views.editCategory , name='edit-category'),
     path('menu-builder/category/delete/<int:pk>' , views.deleteCategory , name='delete-category')
]
from django.urls import path
from . import views
from accounts import views as AccountViews
urlpatterns = [
    path('',AccountViews.vendorDashboard , name = 'vendorDashboard' ),
    path('profile/' , views.profile , name = 'vendor-profile'),
    path('menu-builder/' , views.menuBuilder , name = 'menu-builder'),

    # Catgory CRUD
    path('menu-builder/category/<int:pk>/' , views.foodItemsByCategory , name = 'food-items-by-category'),
    path('menu-builder/category/add/' , views.addCategory , name='add-category'),
    path('menu-builder/category/edit/<int:pk>' , views.editCategory , name='edit-category'),
    path('menu-builder/category/delete/<int:pk>' , views.deleteCategory , name='delete-category'),

    # Food Item Crud
    path('menu-builder/food-item/add/' , views.addFoodItem , name = 'add-food-item'),
    path('menu-builder/food-item/edit/<int:pk>' , views.editFoodItem , name = 'edit-food-item'),
    path('menu-builder/food-item/delete/<int:pk>' , views.deleteFoodItem , name = 'delete-food-item')
]
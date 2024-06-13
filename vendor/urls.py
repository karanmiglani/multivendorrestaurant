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
    path('menu-builder/food-item/delete/<int:pk>' , views.deleteFoodItem , name = 'delete-food-item'),

    # Opening Hours Crud
    path('opening-hours/' , views.openingHours , name = 'opening-hours'),
    path('opening-hours/add' , views.addOpeningHours , name = 'add-opening-hours'),
    path('opening-hours/remove/<int:id>' , views.removeHours , name = 'remove-opening-hours'),

    # dashboard
    path('vendor-order-details/<oid>' , views.orderDetails , name = 'vendor-order-details'),
    path('my-orders',views.myOrders , name = 'vendor-my-orders')


]
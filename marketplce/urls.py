from django.urls import path,include
from . import views

urlpatterns = [

    path('' , views.marketPlace , name = 'market-place'),
    path('<slug:slug>' ,views.vendorDetails , name = 'vendor-details'),

    # Cart
    path('add-to-cart/<int:p_id>/', views.addToCart , name = 'add-to-cart'),
    path('decrease-cart/<int:p_id>' , views.decreaseFromCart , name = 'decrease-cart'),
    path('delete-cart-item/<int:cart_id>',views.deleteCartItem,name='delete-cart-item'),
    path('cart/', views.cart , name = 'cart'),

]
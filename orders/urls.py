from django.urls import path,include
from . import views
urlpatterns = [
    path('place-order/' , views.placeOrder  , name='place-order'),
    path('payment/<oid>' , views.payment  , name='payment'),
    path('complete-order/<oid>/<txn_id>' , views.completeOrder  , name='complete-order'),
]
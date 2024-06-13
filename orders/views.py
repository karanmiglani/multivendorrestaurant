from collections import defaultdict
from decimal import Decimal
from django.shortcuts import render , redirect
from marketplce.views import Cart
from onlinefood_main.context_processor import getCartAmount
from .forms import OrderForm
from .models import OrderModel , Payment , OrderedFood
from menu.models import Product 
from marketplce.models import Tax
import simplejson as json
from .utils import generate_order_number , generate_transaxtion_id
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.
def placeOrder(request):

    cartItems = Cart.objects.filter(user = request.user).select_related('product__vendor')
    if cartItems.count() <= 0:
        return redirect('market-place')
    get_tax_data = Tax.objects.filter(is_active = True)
    # Initialize data structures
    vendor_ids = set()
    vendor_subtotal = defaultdict(float)
    total_data = {}
    subtotal = 0
    for item in cartItems:
        vendor_id = item.product.vendor.id
        vendor_ids.add(vendor_id)
        subtotal = float(item.qty * item.product.price)
        vendor_subtotal[vendor_id] += subtotal
        tax_dict = {}
        for i in get_tax_data:
            tax_type = i.tax_type
            tax_percenatge = i.tax_percentage
            tax_amount = round((vendor_subtotal[vendor_id] * float(tax_percenatge))/100, 2)
            tax_dict.update({tax_type:{str(tax_percenatge) : str(tax_amount)}})
        total_data.update({vendor_id:{str(vendor_subtotal[vendor_id]): str(tax_dict)}})
    subTotal = getCartAmount(request)['subTotal']
    totalTax = getCartAmount(request)['tax']
    grandTotal = getCartAmount(request)['grandTotal']
    tax_data = getCartAmount(request)['tax_dict']
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = OrderModel()
            order.user = request.user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email'].lower()
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.total = grandTotal
            order.tax_data = json.dumps(tax_data)
            order.total_tax = totalTax
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            order.order_number = generate_order_number(request , pk =order.id)
            order.vendors.add(*vendor_ids)
            order.total_data = json.dumps(total_data)
            order.save()
            context = {
                'order' : order,
                'cart_item' : cartItems
            }
            return render(request , 'orders/place_orders.html' , context)
        else:
            print(form.errors)
    return render(request, 'orders/place_orders.html')


def payment(request , oid):
    order = OrderModel.objects.get(order_number = oid)
    # Store payement details in payment model
    txn_id = generate_transaxtion_id(request)
    payment = Payment(user = request.user ,tranaction_id = txn_id , payment_method = order.payment_method , amount = order.total , status = 'Completed')
    payment.save()
    # Update the order model
    order.is_ordered = True
    order.payment = payment
    order.save()
    # Move the cart item to ordered food model
    cartItems = Cart.objects.filter(user = request.user)
    for item in cartItems:
        orderedFood = OrderedFood(order = order , payment = payment , user = request.user , foodItem = item.product , qty = item.qty, price = item.product.price, amount = item.product.price * item.qty )
        orderedFood.save()
    #send order confirmation email to the customer
    #send order recieve email to the vendor
    # Clear the cart on payment successfull
    cartItems.delete()
    return redirect(reverse('complete-order', kwargs={'oid':oid,'txn_id':txn_id}))

def completeOrder(request , oid , txn_id):
    try:
        order = OrderModel.objects.get(order_number = oid, payment__tranaction_id = txn_id ,is_ordered = True)
        ordered_food = OrderedFood.objects.filter(order = order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.qty)
        tax_data = json.loads(order.tax_data)

        context = {
        'order_number' : oid,
        'txn_id' : txn_id,
        'order' : order,
        'orderedFood' : ordered_food,
        'subTotal' : subtotal,
        'tax_data':tax_data
    }
        return render(request , 'orders/complete_order.html', context)
    except Exception as e:
        print('Error is')
        print(str(e))
        return redirect('home')
    
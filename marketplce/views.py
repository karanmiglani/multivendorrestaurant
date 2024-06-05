from django.shortcuts import render , redirect , get_object_or_404
from vendor.models import Vendor
from menu.models import Category , Product
from django.db.models import Prefetch
from django.http import  JsonResponse ,HttpResponse
from .models import Cart
from onlinefood_main.context_processor import getCartCounter , getCartAmount
from django.contrib.auth.decorators import login_required
from vendor.models import OpeningHours
from datetime import date , datetime
# Create your views here.
def marketPlace(request):
    vendors = Vendor.objects.filter(is_approved =  True , user__is_active = True)
    vendor_count = vendors.count()
    context = {
        'vendors' :vendors,
        'vendor_count' : vendor_count
    }
    return render(request , 'marketplace/listings.html' , context)


def vendorDetails(request , slug):
    vendor = get_object_or_404(Vendor , slug = slug)
    categories = Category.objects.filter(vendor = vendor).prefetch_related(
        Prefetch(
            'product',
            queryset = Product.objects.filter(is_available = True)
        )
    )
    opening_hours = OpeningHours.objects.filter(vendor = vendor.id).order_by('day','from_hours')
    # check current date
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHours.objects.filter(vendor = vendor.id , day = today)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user = request.user)
    else:
        cart_items = None
    context = {
        'vendor' : vendor,
        'categories' : categories,
        'cart_items': cart_items,
        'opening_hours' : opening_hours,
        'current_opening_hour' : current_opening_hours,
    }
    return render(request , 'marketplace/vendor_details.html' , context)


def addToCart(request , p_id):
    
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                print('cart amount is' ,getCartAmount(request))
                product = Product.objects.get(id = p_id)
                # check the user if already added to cart 
                try:
                    print('Hello')
                    checkCart = Cart.objects.get(user = request.user , product = product )
                    # Increase quantity
                    checkCart.qty += 1
                    checkCart.save()
                    
                    return JsonResponse({'status' : 200,'message': 'Item added to cart' , 'cart_counter' : getCartCounter(request) ,'qty':checkCart.qty ,'cart_amount' : getCartAmount(request)})
                except:
                    checkCart = Cart.objects.create(user = request.user , product = product , qty = 1)        
                    return JsonResponse({'status' : 200,'message': 'New Item added to cart','cart_counter' : getCartCounter(request) , 'qty':checkCart.qty , 'cart_amount' : getCartAmount(request)})
            except Exception as e:
                print(str(e))
                return JsonResponse({'status' : 404,'message': 'This item doesnot exists'})    

        else:
            return JsonResponse({'status' : 404,'message': 'Inavlid Request'})
    return JsonResponse({'status' : 404,'message': 'Please login to continue'})



def decreaseFromCart(request , p_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = Product.objects.get(id = p_id)
               
                try:
                    checkCart = Cart.objects.get(user = request.user , product = product)
                    
                    if checkCart.qty > 1:
                        checkCart.qty -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.qty = 0
                    return JsonResponse({'status' : 200,'message': 'Cart Updated!' , 'cart_counter':getCartCounter(request),'qty':checkCart.qty,'cart_amount' : getCartAmount(request)})     
                except:
                    return JsonResponse({'status' : 204,'message': 'You don\'t have item in your cart!'})     
            except:
                return JsonResponse({'status' : 404,'message': 'This item doesnot exists'})    
        else:
            return JsonResponse({'status' :400 ,'message': 'Inavlid Request'})
    return JsonResponse({'status' : 401,'message': 'Please login to continue'})

def deleteCartItem(request , cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if item in cart exists
                cartItem = Cart.objects.get(user = request.user , id = cart_id)
                if cartItem:
                    cartItem.delete()
                    return JsonResponse({'status' : 200,'message': 'Cart Item deleted' , 'cart_counter' :  getCartCounter(request) , 'cart_amount' : getCartAmount(request)})    
            except:
                return JsonResponse({'status' : 404,'message': 'This item doesnot exists'})    
        else:
            return JsonResponse({'status' :400 ,'message': 'Inavlid Request'})
    return JsonResponse({'status' : 401,'message': 'Please login to continue'})




@login_required(login_url='logi')
def cart(request):
    cartItems = Cart.objects.filter(user = request.user).order_by('created_at')
    context = {
        'cartItems':cartItems
    }
    return render(request , 'marketplace/cart.html',context)


def search(request):
    return HttpResponse('Search')

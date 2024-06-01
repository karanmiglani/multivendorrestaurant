# onlinefood_main/context_processor.py
from vendor.models import Vendor
from django.conf import settings
from marketplce.models import Cart
from menu.models import Product

def get_vendor(request):
    if not request.user.is_authenticated:
         return {'vendor': None}
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        vendor = None
    return {'vendor': vendor}


def get_goole_api_key(request):
    return {'GOOGLE_API_KEY' : settings.GOOGLE_API_KEY}



def getCartCounter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user = request.user)
            if cart_items:
                for c in cart_items:
                    cart_count += c.qty
            else:
                cart_count = 0        
        except:
            cart_count = 0
    return dict(cart_count = cart_count)

def getCartAmount(request):
    subTotal = 0
    sgst = 0
    cgst = 0
    grandTotal = 0
    if request.user.is_authenticated:
        try:
            cartItem = Cart.objects.filter(user = request.user)
            for item in cartItem:
                product = Product.objects.get(pk = item.product.id) 
                subTotal = subTotal + (product.price * item.qty)
                print(subTotal)
            grandTotal = subTotal + sgst + cgst
        except:
            subTotal = tax = grandTotal = 0
    print(subTotal)
    return dict(subTotal = subTotal , sgst = sgst , cgst = cgst, grandTotal = grandTotal)

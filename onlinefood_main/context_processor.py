# onlinefood_main/context_processor.py
from vendor.models import Vendor
from django.conf import settings
from marketplce.models import Cart , Tax
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
    return {'ACCESS_TOKEN' : settings.ACCESS_TOKEN}



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
    grandTotal = 0
    tax_dict = {}
    tax = 0
    if request.user.is_authenticated:
        try:
            cartItem = Cart.objects.filter(user = request.user)
            for item in cartItem:
                product = Product.objects.get(pk = item.product.id) 
                subTotal = subTotal + (product.price * item.qty)
            get_tax = Tax.objects.filter(is_active = True)
            for i in get_tax:
                tax_type = i.tax_type
                tax_percentage = i.tax_percentage
                tax_amount = round((tax_percentage * subTotal) / 100,2)
                tax_percentage_str = str(tax_percentage)
                if tax_type in tax_dict:
                    tax_dict[tax_type][tax_percentage_str] = tax_amount
                else:
                    tax_dict[tax_type]  = {tax_percentage_str:tax_amount}
            

            # Calculate the total tax
            for tax_type , tax_percentages in tax_dict.items():
                for tax_percentage_str , tax_amount in tax_percentages.items():
                    tax = tax + tax_amount
            grandTotal = subTotal + tax
        except Exception as e:
            print(str(e))
            subTotal = tax = grandTotal = 0
    return dict(subTotal = subTotal ,  grandTotal = grandTotal , tax = tax , tax_dict = tax_dict)

from .models import Cart
from menu.models import Product

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
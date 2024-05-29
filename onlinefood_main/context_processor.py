# onlinefood_main/context_processor.py
from vendor.models import Vendor

def get_vendor(request):
    if not request.user.is_authenticated:
         return {'vendor': None}
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        vendor = None
    return {'vendor': vendor}

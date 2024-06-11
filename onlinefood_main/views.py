from django.shortcuts import render
from django.http import HttpResponse
from vendor.views import Vendor

def home(request):
    vendor = Vendor.objects.filter(is_approved=True , user__is_active = True)[:8]
    distances = range(5,105,5)
    context = {
        'vendor' : vendor,
        'distances' : distances
    }
    return render(request,'home.html' , context)
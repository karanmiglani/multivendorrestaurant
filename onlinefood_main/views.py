from django.shortcuts import render
from django.http import HttpResponse
from vendor.views import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance


def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        long = request.session['long']
        return long , lat
    elif 'lat' in request.GET:
        lat = request.GET['lat'] 
        long = request.GET['long']
        request.session['lat'] = lat
        request.session['long'] = long
        return long , lat
    else:
        return None

def home(request):
    if get_or_set_current_location(request) is not None:
        pnt = GEOSGeometry('POINT(%s %s)'%(get_or_set_current_location(request)))
        vendor  = Vendor.objects.filter(user_profile__location__distance_lte = (pnt , D(km = 150))).annotate(distance = Distance('user_profile__location', pnt)).order_by('distance')
        for v in vendor:
            v.kms = round(v.distance.km,1)
    else:
        vendor = Vendor.objects.filter(is_approved=True , user__is_active = True)[:8]
    distances = range(5,105,5)
    context = {
        'vendor' : vendor,
        'distances' : distances
    }
    return render(request,'home.html' , context)
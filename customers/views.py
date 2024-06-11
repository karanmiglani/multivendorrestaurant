from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def customerProfile(request):
    print(request.path)
    return render(request , 'customer/profile.html')

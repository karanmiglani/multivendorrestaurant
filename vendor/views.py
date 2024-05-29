from django.shortcuts import render

# Create your views here.
def profile(request):
    print(request.path)
    return render(request , 'vendor/profile.html')
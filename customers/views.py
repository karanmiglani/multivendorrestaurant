from django.shortcuts import render,get_object_or_404 , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm , UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
# Create your views here.


@login_required(login_url='login')
def customerProfile(request):
    profile = get_object_or_404(UserProfile , user = request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST , request.FILES , instance = profile)
        user_form = UserInfoForm(request.POST , instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.add_message(request , messages.SUCCESS , 'Profile Update Successfuly!')
            return redirect('customer-profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profileForm = UserProfileForm(instance = profile)
        userForm = UserInfoForm(instance=request.user)
    context = {
        'profile_form' : profileForm,
        'user_form' : userForm,
        'profile' :profile

    }
    return render(request , 'customer/profile.html' , context)

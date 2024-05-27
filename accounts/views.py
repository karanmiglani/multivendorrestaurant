from django.shortcuts import render , redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user = form.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email'].lower()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user = User.objects.create_user(first_name=first_name , last_name=last_name , email=email , username=username,password=password)
            user.role = User.CUSTOMER
            user.phone_number = phone_number
            user.save()
            messages.add_message(request , messages.SUCCESS , 'Your account has been registered successfully!')
            return redirect('register-user')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {'form' : form}
    return render(request , 'accounts/register_user.html',context)


def registerVendor(request):
    if request.method == "POST":
        userForm = UserForm(request.POST)
        form = VendorForm(request.POST , request.FILES)
        if userForm.is_valid() and form.is_valid():
            first_name = userForm.cleaned_data['first_name']
            last_name = userForm.cleaned_data['last_name']
            phone_number = userForm.cleaned_data['phone_number']
            email = userForm.cleaned_data['email']
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name , last_name=last_name , email=email , username=username,password=password)
            user.role = User.VENDOR
            user.phone_number = phone_number
            user.save()
            vendor = form.save(commit=False)
            vendor.user = user
            print('Getting user profile')
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            print('user profile id is: ',user_profile)
            vendor.save()
            messages.add_message(request , messages.SUCCESS , 'Your account has been registered with us! Please wait for the admin approval.')
            return redirect('register-user')
        else:
            print('invalid_form')
            print('Error')
    else:
        userForm = UserForm()
        form = VendorForm()
    context = {'form' : form,'user_form' :userForm}
    return render(request , 'accounts/register_vendor.html',context)
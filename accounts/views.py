from django.shortcuts import render , redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required , user_passes_test
from .utils import detectUser
from django.core.exceptions import PermissionDenied
# Create your views here.

# restrict vendor from accessing the cutomer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# restrict cutomer from accessing the vendor page

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.add_message(request , messages.WARNING , 'You are already registered!')
        return redirect('dashboard')
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.add_message(request , messages.WARNING , 'You are already registered!')
        return redirect('dashboard')
    elif request.method == "POST":
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


def login(request):
    if request.user.is_authenticated:
        messages.add_message(request , messages.WARNING , 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email , password = password)

        if user is not None:
            auth.login(request , user)
            messages.add_message(request , messages.SUCCESS , 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.add_message(request , messages.ERROR , 'Invalid login credentials')
            return redirect('login')
    return render(request , 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.add_message(request , messages.INFO , 'You are logged out.')
    return redirect('login')


@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request , 'accounts/customer_dashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request , 'accounts/vendor_dashboard.html')
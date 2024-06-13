from django.shortcuts import render , redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required , user_passes_test
from .utils import detectUser , send_verification_mail 
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from orders.models import OrderModel
import datetime
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
            # Send verification email
            mail_subject = 'Activate your account'
            template_name = 'accounts/emails/account_verification_email.html'
            send_verification_mail(request , user , mail_subject , template_name)
            messages.add_message(request , messages.SUCCESS , 'Your account has been registered successfully! Please check your mail to activate your account')
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
        return redirect('myAccount')
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
            mail_subject = 'Activate your account'
            template_name = 'accounts/emails/account_verification_email.html'
            # send_verification_mail(request , user , mail_subject , template_name)
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


def activate(request , uidb64 , token):
    # Activate the user by setting is_active status as true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print('Uid is :' , uid)
        user = User._default_manager.get(pk=uid)
        
    except(TypeError , ValueError , OverflowError , User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user , token):
        user.is_active = True
        user.save()
        messages.add_message(request , messages.SUCCESS , 'Congartulations! your account has been activated')
        return redirect('myAccount')
    else:
        messages.add_message(request , messages.ERROR , 'Invalid Token!')
        return redirect('myAccount')

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


def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']

        if User.objects.filter(email = email).exists():
            user = User.objects.get(email__exact = email)
            # send reset password email
            mail_subject = 'Reset your password'
            template_name = 'accounts/email/reset_password_email.html'
            send_verification_mail(request , user , mail_subject , template_name)
            messages.add_message(request , messages.SUCCESS , 'Password reset link has been sent to your registered email address')
            return redirect('login')
        else:
            messages.add_message(request , messages.ERROR , 'Account does not exists')
            return redirect('forgot-password')
    return render(request , 'accounts/forgot_password.html')


def resetPasswordValidate(request , uidb64 , token):
    # validate user token
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError , ValueError , OverflowError , User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user , token):
       request.session['uid'] = uid
       messages.add_message(request , messages.INFO , 'Please reset your password')
       return redirect('reset-password')
    else:
        messages.add_message(request , messages.ERROR , 'This link has been expired')
        return redirect('myAccount')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk = pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.add_message(request , messages.SUCCESS , 'Password reset successful')
            return redirect('login')
        else:
            messages.add_message(request , messages.ERROR , 'Password and confirm does not match')
            return redirect('reset-password')
    return render(request , 'accounts/reset_password.html')

@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    orders = OrderModel.objects.filter(user = request.user , is_ordered = True)
    recent_order = orders[:5]
    context = {
        'orders' : orders,
        'orders_count' : orders.count(),
        'recent_orders' : recent_order
    }
    return render(request , 'accounts/customer_dashboard.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user = request.user)
    orders = OrderModel.objects.filter(vendors__in=[vendor.id] , is_ordered = True).order_by('-created_at')
    recent_orders = orders[:10]
    current_month =  datetime.datetime.now().month
    current_month_orders = orders.filter(vendors__in = [vendor.id] , created_at__month = current_month)
    current_month_revenue = 0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grandTotal']
    print(current_month_revenue)
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grandTotal']
    context = {
        'orders' : orders,
        'order_count_total' : orders.count(),
        'recent_orders' : recent_orders,
        'total_revenue' : total_revenue,
        'current_month_revenue' : current_month_revenue
    }
    return render(request , 'accounts/vendor_dashboard.html', context)


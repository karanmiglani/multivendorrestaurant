from django.shortcuts import render,get_object_or_404 , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm , UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import OrderModel , OrderedFood
import simplejson as json
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


def myOrders(request):
    orders = OrderModel.objects.filter(user = request.user , is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request , 'customer/my_orders.html' , context)


def orderDetails(request,order_number):
    order = OrderModel.objects.get(order_number = order_number , is_ordered = True)
    ordered_food = OrderedFood.objects.filter(order = order)
    subTotal = 0
    for item in ordered_food:
        subTotal += (item.qty * item.foodItem.price)
    tax_data = json.loads(order.tax_data)
    context = {
        'order' : order,
        'orderedFood' : ordered_food,
        'subTotal' : subTotal,
        'tax_data' : tax_data
        
    }
    return render(request , 'customer/order_detail.html', context)

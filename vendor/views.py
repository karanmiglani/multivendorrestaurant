from django.shortcuts import render , get_object_or_404 ,redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category , Product
from menu.forms import CategoryForm, ProductForm
from django.template.defaultfilters import slugify
from.errors import handle_category_name_unique_constraints , handle_product_unique_constraints
from django.db import IntegrityError
# Create your views here.

def getVendor(request):
    vendor = Vendor.objects.get(user = request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def profile(request):
    profile = get_object_or_404(UserProfile , user = request.user)
    vendor = get_object_or_404(Vendor , user = request.user)
    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES , instance=profile)
        vendor_form = VendorForm(request.POST , request.FILES , instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.add_message(request , messages.SUCCESS , 'Profile Updated Successfuly')
            return redirect('vendor-profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)

    context = {
        'profile_form' :profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor
    }
    return render(request , 'vendor/profile.html' ,context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor = getVendor(request)
    print('Vendor' , vendor)
    categories = Category.objects.filter(vendor = vendor).order_by('created_at')
    context = {
        'category' : categories
    }
    return render(request , 'vendor/menu_builder.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def foodItemsByCategory(request , pk=None):
    vendor = getVendor(request)
    category = get_object_or_404(Category , pk=pk )
    food_items = Product.objects.filter(vendor = vendor , category = category)
    context = {
        'foodItems' :food_items ,
        'category' : category
    }
    return render(request , 'vendor/foodItemsByCategory.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def addCategory(request):
    if request.method == 'POST':
       form = CategoryForm(request.POST)
       if form.is_valid():
           category_name = form.cleaned_data['category_name']
           category_name = category_name.title()
           category = form.save(commit=False)
           category.vendor = getVendor(request)
           if handle_category_name_unique_constraints(request , category_name ,getVendor(request)):
               form.save()
               messages.add_message(request , messages.SUCCESS , 'Category created successfully!')
               return redirect('menu-builder')
    else:
        form = CategoryForm()
    
    context = {
        'form' : form
    }
    return render(request , 'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def editCategory(request , pk=None):
    category = get_object_or_404(Category , pk = pk)
    if request.method == "POST":
        form = CategoryForm(request.POST , instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category_name = category_name.title()
            category = form.save(commit=False)
            category.vendor = getVendor(request)
            if handle_category_name_unique_constraints(request , category_name=category_name , vendor=getVendor(request)):
                form.save()
                messages.add_message(request , messages.SUCCESS , 'Category Updated Successfuly!')
                return redirect('menu-builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {
        'form' : form,
        'category' :category
    }
    return render(request , 'vendor/edit_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def deleteCategory(request , pk):
    category = get_object_or_404(Category , pk = pk)
    category.delete()
    messages.add_message(request , messages.SUCCESS , 'Category Deleted Successfuly')
    return redirect('menu-builder')

# Food Item CRUD

def addFoodItem(request):
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES)
        if form.is_valid():
            category = form.cleaned_data['category']
            product_title = form.cleaned_data['product_title']
            product_title = product_title.title()
            try:
                food = form.save(commit=False)
                food.vendor=getVendor(request)
                form.save()
                messages.add_message(request , messages.SUCCESS , 'Item added successfully')
                return redirect('food-items-by-category' ,food.category.id )
            except IntegrityError:
                form.add_error(None , 'Product with this category and item name already exists')
                
        else:
            print(form.errors)
    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.filter(vendor = getVendor(request))
    context = {
        'form' : form
    }
    return render(request , 'vendor/add_food_item.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def editFoodItem(request , pk=None):
    foodItem = get_object_or_404(Product , pk = pk)
    form = ProductForm(instance=foodItem)
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES , instance=foodItem)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product_title = product_title.title()
            try:
                food = form.save(commit=False)
                food.vendor = getVendor(request)
                form.save()
                messages.add_message(request , messages.SUCCESS , 'Product details updated successfuly!')
                return redirect('food-items-by-category' ,food.category.id)
            except IntegrityError:
                form.add_error(None , 'Product with this category and item name already exists')
        else:
            print(form.errors)
        
    context = {
        'form' : form,
        'foodItem' : foodItem
    }
    return render(request , 'vendor/edit_food_item.html' , context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def deleteFoodItem(request , pk):
    product = get_object_or_404(Product , pk = pk)
    product.delete()
    messages.add_message(request , messages.SUCCESS , 'Item Deleted Successfuly')
    return redirect('food-items-by-category' ,product.category.id)

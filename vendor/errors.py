from django.contrib import messages
from django.db import IntegrityError
from menu.models import Category,Product

def handle_category_name_unique_constraints(request , category_name , vendor):
    try:
       if  Category.objects.get(category_name = category_name , vendor = vendor):
        messages.add_message(request , messages.ERROR , 'Category with this name already exists..')   
    except Category.DoesNotExist:
       return True


def handle_product_unique_constraints(request , category , vendor , product_title):
   try:
        if Product.objects.get(vendor = vendor , category = category , product_title = product_title):
           messages.add_message(request , messages.ERROR , 'Product with this category and item name already exists..')
           return False
   except Product.DoesNotExist:
      True

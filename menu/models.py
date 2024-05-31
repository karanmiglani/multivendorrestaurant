from django.db import models
from vendor.models import Vendor
from django.template.defaultfilters import slugify
# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    description = models.TextField(max_length=500 , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        constraints = [
            models.UniqueConstraint(fields=['vendor' , 'category_name' ,'slug'],name='unique_vendor_category_name_slug')
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            # Object is being created for the first time
            super().save(*args, **kwargs)  # Save the object to generate an ID
            vendor_name = slugify(self.vendor.vendor_name)
            self.slug = f"{slugify(self.category_name)}-{vendor_name}"  # Update slug with ID
            self.save(update_fields = ['slug'])  # Print slug here to verify
        else:
            super().save(*args, **kwargs)  # For updating existing objects

    def clean(self):
        self.category_name = self.category_name.title()
    def __str__(self):
        return self.category_name

       
    


class Product(models.Model):
    vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    product_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=500 , blank=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    image = models.ImageField(upload_to='products')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vendor' , 'category' , 'product_title'] , name='unique_vendor_category_product_title')
        ]


    def __str__(self):
        return self.product_title
    
    def clean(self):
        self.product_title = self.product_title.title()
    
    def save(self , *args , **kwargs):
        vendor_name = slugify(self.vendor.vendor_name)
        self.slug = f"{slugify(self.product_title)}-{vendor_name}" 
        self.clean()
        super().save(*args , **kwargs)
    
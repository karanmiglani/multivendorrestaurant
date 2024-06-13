from django.db import models
from accounts.models import User
from marketplce.models import Product 
from vendor.models import Vendor
import simplejson as json
# Create your models here.


request_object = ''

class Payment(models.Model):
    PAYMENT_METHOD =(
        ('Paypal' , 'Paypal'),
        ('RazorPay', 'RazorPay')
    )

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    tranaction_id = models.CharField(max_length=500)
    payment_method = models.CharField(choices=PAYMENT_METHOD , max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tranaction_id



class OrderModel(models.Model):
    STATUS = (
        ('New' , 'New'),
        ('Accepted','Accepted'),
        ('Completed' , 'Completed'),
        ('Cancelled' , 'Cancelled'),
    )
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    payment = models.ForeignKey(Payment , on_delete=models.CASCADE , blank=True , null=True)
    vendors = models.ManyToManyField(Vendor ,blank=True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50 , blank=True)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text="Data Format:{'tax_type' : {'tax_percentage':'tax_amount'}}")
    total_data = models.JSONField(blank=True , null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=50)
    order_status = models.CharField(max_length=50 ,choices=STATUS , default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
    
    def order_placed_to(self):
        return ",".join([str(i) for i in self.vendors.all()])
    
    def get_total_by_vendor(self):
        try:
            vendor = Vendor.objects.get(user = request_object.user)
            subTotal = 0.0
            tax = 0
            tax_dict = {}
            if self.total_data:
                total_data = json.loads(self.total_data)
                data = total_data.get(str(vendor.id))
                
                for key , value in data.items():
                    key = float(key)
                    subTotal = subTotal + float(key)
                    value = value.replace("'",'"')
                    value = json.loads(value)
                    tax_dict.update(value)
                    for i in value:
                        for j in value[i]:
                            print(value[i][j])
                            tax += float(value[i][j])
                grandTotal = float(subTotal) + float(tax)
            context = {
                'subTotal' : subTotal,
                'tax_dict' : tax_dict,
                'tax' : tax,
                'grandTotal' : grandTotal

            }
        except Exception as e:
            print('error',str(e))
        return context
        
    
    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(OrderModel , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment , on_delete=models.SET_NULL , blank=True , null=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    foodItem = models.ForeignKey(Product , on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.foodItem.product_title

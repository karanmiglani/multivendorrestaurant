from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager,UserManager
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self , first_name , last_name ,username , email , password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self , first_name , last_name , username , email , password = None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using = self._db)
        return user

    


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (VENDOR  , 'Restaurant'),
        (CUSTOMER , 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50 , unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES , blank=True , null=True)

    # Required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",'first_name','last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self , permission , obj = None):
        return self.is_admin
    
    def has_module_perms(self , app_lable):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Restaurant'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

class UserProfile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='user/profile_pictures',blank=True , null=True)
    cover_photo = models.ImageField(upload_to='user/cover_photo',blank=True , null=True)
    address_line_1 =  models.CharField(max_length=50,blank=True,null=True)
    address_line_2 =  models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.CharField(max_length=6,blank=True,null=True)
    latitude = models.CharField(max_length=20,blank=True,null=True)
    longitude = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email
    
    def full_address(self):
        if self.address_line_1 and self.address_line_2 is not None:
            return f'{self.address_line_1} , {self.address_line_2}'
        elif self.address_line_1 is not None and self.address_line_2 is None:
            return f'{self.address_line_1}'
        elif self.address_line_1 is None and self.address_line_2 is not None:
            return f'{self.address_line_2}'


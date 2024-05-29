from django.db import models
from accounts.models import User , UserProfile
from accounts.utils import send_notification
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=True , null=True , related_name='user')
    user_profile = models.OneToOneField(UserProfile , on_delete=models.CASCADE , related_name='user_profile')
    vendor_name = models.CharField(max_length=150)
    vendor_licence = models.ImageField(upload_to='vendor/liscence')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.vendor_name
    
    def save(self , *args , **kwargs):
        if self.pk is not None:
            vendor = Vendor.objects.get(pk = self.pk)
            if vendor.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                        'user' : self.user,
                        'is_approved': self.is_approved
                    }
                if self.is_approved == True:
                    # send 
                    mail_subject = 'Congratulation your restaurant has been aprroved!'
                    send_notification(mail_subject , mail_template , context)
                else:
                    mail_subject = 'Sorry! You are not eligible for publishing food menu on our marketplace'
                    send_notification(mail_subject , mail_template , context)
        
        return super(Vendor , self).save(*args , **kwargs)
    

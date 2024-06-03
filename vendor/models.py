from django.db import models
from accounts.models import User , UserProfile
from accounts.utils import send_notification
from django.template.defaultfilters import slugify
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from datetime import time , datetime , date
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=True , null=True , related_name='user')
    user_profile = models.OneToOneField(UserProfile , on_delete=models.CASCADE , related_name='user_profile')
    vendor_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=500 , unique=True)
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
        self.slug = f"{slugify(self.vendor_name)}-{urlsafe_base64_encode(force_bytes(self.user.id))}"
        return super(Vendor , self).save(*args , **kwargs)
    
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday() #returns moonday as 1 , tuesday  as 2
        current_opening_hours = OpeningHours.objects.filter(vendor = self , day=today)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        is_open = None
        for i in current_opening_hours:
            start = str(datetime.strptime(i.form_hours,"%I:%M %p").time())
            end = str(datetime.strptime(i.to_hours,"%I:%M %p").time())
            if current_time > start and current_time < end :
                is_open = True
                break
            else:
                is_open = False
        return is_open
        


DAYS  = [
    (1 , 'Monday'),
    (2 , 'Tuesday'),
    (3 , 'Wednesday'),
    (4 , 'Thursday'),
    (5 , 'Friday'),
    (6 , 'Saturday'),
    (7 , 'Sunday'),
]
HOURS_OF_DAYS_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(24) for m in (0, 30)]
class OpeningHours(models.Model):
    vendor = models.ForeignKey(Vendor , on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hours = models.CharField(choices=HOURS_OF_DAYS_24 , max_length=10 , blank=True)
    to_hours = models.CharField(choices=HOURS_OF_DAYS_24 , max_length=10 , blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day' , 'from_hours')
        constraints = [
            models.UniqueConstraint(fields=['vendor','day','from_hours','to_hours'] , name='unique_opening_hour')
        ]
    
    def __str__(self):
        return self.get_day_display()
    

    
    

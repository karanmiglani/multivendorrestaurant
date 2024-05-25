from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User , UserProfile

@receiver(post_save , sender = User)
def post_save_create_profile_receiver(sender , instance , created , **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("User profile is created")
    else:
        try:
            profile = UserProfile.objects.get(user = instance)
            profile.save()
            print("User profile is updated")
        except:
            # Create user profile if not exist
            UserProfile.objects.create(user=instance)
            print("User profile is created but not exist")

@receiver(pre_save , sender = User)
def pre_save_profile_receiver(sender , instance , **kwargs):
    print(instance.username , 'this user is saving')
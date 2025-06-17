from django.db.models.signals import post_save
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import Profile 

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile for a new user, or just save the existing one.
    """
    if created:
        # If the User was just created, create a corresponding Profile.
        Profile.objects.create(user=instance)
    
    instance.profile.save()
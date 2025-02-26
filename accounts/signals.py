from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, FarmerProfile, ExpertProfile
from admin_dash.models import UserApproval

@receiver(post_save, sender=CustomUser)
def create_profile_and_approval(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.admin_registered:  # Skip admins and admin-registered users
        if instance.role == 'farmer':
            FarmerProfile.objects.get_or_create(user=instance)
        elif instance.role == 'agricultural_expert':
            ExpertProfile.objects.get_or_create(user=instance)
        # Only create UserApproval for regular signups
        UserApproval.objects.get_or_create(user=instance)
    elif created and not instance.is_superuser and instance.admin_registered:
        # Still create profile for admin-registered users, but no UserApproval
        if instance.role == 'farmer':
            FarmerProfile.objects.get_or_create(user=instance)
        elif instance.role == 'agricultural_expert':
            ExpertProfile.objects.get_or_create(user=instance)
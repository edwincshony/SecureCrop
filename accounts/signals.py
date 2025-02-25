from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, FarmerProfile, ExpertProfile
from admin_dash.models import UserApproval

@receiver(post_save, sender=CustomUser)
def create_profile_and_approval(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:  # Skip for admins
        if instance.role == 'farmer':
            FarmerProfile.objects.create(user=instance)
            UserApproval.objects.create(user=instance)
        elif instance.role == 'agricultural_expert':
            ExpertProfile.objects.create(user=instance)
            UserApproval.objects.create(user=instance)
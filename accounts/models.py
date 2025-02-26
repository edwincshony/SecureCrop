from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('agricultural_expert', 'Agricultural_expert'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    admin_registered = models.BooleanField(default=False)  # New field to flag admin-registered users

    def __str__(self):
        return self.username

class FarmerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    location = models.CharField(max_length=100, blank=True)
    crop_types = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Farmer Profile"

class ExpertProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='expert_profile')
    expertise = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Expert Profile"
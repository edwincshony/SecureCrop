from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FarmerProfile, ExpertProfile

admin.site.register(CustomUser, UserAdmin)
admin.site.register(FarmerProfile)
admin.site.register(ExpertProfile)
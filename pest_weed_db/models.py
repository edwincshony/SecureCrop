from django.db import models

class Pest(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    symptoms = models.TextField()
    control_measures = models.TextField()
    image = models.ImageField(upload_to='pests/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Weed(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    symptoms = models.TextField()  # Effects on crops
    control_measures = models.TextField()
    image = models.ImageField(upload_to='weeds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Crop(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    growing_conditions = models.TextField()
    common_diseases = models.TextField()
    best_practices = models.TextField()
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
from django.db import models
from accounts.models import CustomUser
from pest_weed_db.models import Crop

class CropLifecycle(models.Model):
    STAGE_CHOICES = [
        ('planting', 'Planting Stage'),
        ('watering', 'Watering Schedule'),
        ('fertilizer', 'Fertilizers Used'),
        ('sunlight', 'Sunlight & Environmental Needs'),
        ('harvesting', 'Harvesting'),
        ('post_harvest', 'Post-Harvest Practices'),
    ]

    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='lifecycle')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} - {self.get_stage_display()} on {self.date}"


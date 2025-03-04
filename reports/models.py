from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date

class PestSighting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pest_sightings")
    crop = models.ForeignKey('pest_weed_db.Crop', on_delete=models.CASCADE, related_name='pest_sightings', blank=True, null=True)
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # Add missing fields
    symptoms_recap = models.TextField(blank=True, null=True)
    identification_confirmation = models.BooleanField(default=False)
    next_steps = models.TextField(blank=True, null=True)
    control_measures = models.TextField(blank=True, null=True)
    educational_nugget = models.TextField(blank=True, null=True)
    pest_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Sighting by {self.user.username} on {self.date}"



class TreatmentOutcome(models.Model):
    EFFECTIVENESS_CHOICES = [
        ('effective', 'Effective'),
        ('partially_effective', 'Partially Effective'),
        ('ineffective', 'Ineffective'),
    ]

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)  # Ensure this is correctly referenced
    pest = models.ForeignKey('pest_weed_db.Pest', on_delete=models.CASCADE)
    crop = models.ForeignKey('pest_weed_db.Crop', on_delete=models.CASCADE, related_name='treatmentoutcome', blank=True, null=True)
    treatment_method = models.CharField(max_length=200)
    date_applied = models.DateField()
    time_applied = models.TimeField(null=True, blank=True, help_text="Optional exact time of treatment")
    effectiveness = models.CharField(max_length=20, choices=EFFECTIVENESS_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Treatment for {self.pest} by {self.user} on {self.date_applied} at {self.time_applied or 'Unknown time'}"

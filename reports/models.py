from django.db import models
from accounts.models import CustomUser
from pest_weed_db.models import Pest

class PestSighting(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.pest.name} sighted by {self.user.username} on {self.date}"

class TreatmentOutcome(models.Model):
    EFFECTIVENESS_CHOICES = [
        ('effective', 'Effective'),
        ('partially_effective', 'Partially Effective'),
        ('ineffective', 'Ineffective'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE)
    treatment_method = models.CharField(max_length=200)
    date_applied = models.DateField()
    effectiveness = models.CharField(max_length=20, choices=EFFECTIVENESS_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Treatment for {self.pest.name} by {self.user.username} on {self.date_applied}"
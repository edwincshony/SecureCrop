from django import forms
from django.core.exceptions import ValidationError
from .models import PestSighting, TreatmentOutcome
from datetime import date

class PestSightingForm(forms.ModelForm):
    class Meta:
        model = PestSighting
        fields = ['pest', 'location', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()}),  # Set max to today's date
            'time': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    def clean_date(self):
        sighting_date = self.cleaned_data['date']
        if sighting_date > date.today():
            raise ValidationError("The date cannot be in the future.")
        return sighting_date

class TreatmentOutcomeForm(forms.ModelForm):
    class Meta:
        model = TreatmentOutcome
        fields = ['pest', 'treatment_method', 'date_applied', 'time_applied', 'effectiveness', 'notes']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()}),  # Set max to today's date
            'time_applied': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    def clean_date_applied(self):
        applied_date = self.cleaned_data['date_applied']
        if applied_date > date.today():
            raise ValidationError("The date applied cannot be in the future.")
        return applied_date
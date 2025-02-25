from django import forms
from .models import PestSighting, TreatmentOutcome

class PestSightingForm(forms.ModelForm):
    class Meta:
        model = PestSighting
        fields = ['pest', 'location', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class TreatmentOutcomeForm(forms.ModelForm):
    class Meta:
        model = TreatmentOutcome
        fields = ['pest', 'treatment_method', 'date_applied', 'effectiveness', 'notes']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
        }
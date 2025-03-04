from django import forms
from django.core.exceptions import ValidationError
from .models import PestSighting, TreatmentOutcome
from datetime import date
from django.apps import apps

# Dynamically get the Crop model from another app
Crop = apps.get_model('pest_weed_db', 'Crop')

class PestSightingForm(forms.ModelForm):
    class Meta:
        model = PestSighting
        fields = ['crop', 'location', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()}),
            'time': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Capture the logged-in user
        super().__init__(*args, **kwargs)

        # Ensure crop is mandatory
        self.fields['crop'].required = True
        self.fields['notes'].required = True


        if user and user.role == 'expert':  # Show expert fields only for experts
            self.fields['pest_name'] = forms.CharField(required=True, label="Identified Pest Name")
            self.fields['identification_confirmation'] = forms.CharField(
                widget=forms.Textarea, required=True, label="Identification Confirmation"
            )
            self.fields['symptoms_recap'] = forms.CharField(
                widget=forms.Textarea, required=True, label="Symptoms Recap"
            )
            self.fields['control_measures'] = forms.CharField(
                widget=forms.Textarea, required=True, label="Control Measures"
            )
            self.fields['next_steps'] = forms.CharField(
                widget=forms.Textarea, required=True, label="Next Steps"
            )
            self.fields['educational_nugget'] = forms.CharField(
                widget=forms.Textarea, required=False, label="Educational Nugget (Optional)"
            )

    def clean_date(self):
        sighting_date = self.cleaned_data.get('date')
        if sighting_date and sighting_date > date.today():
            raise forms.ValidationError("The date cannot be in the future.")
        return sighting_date

    def clean_crop(self):
        crop = self.cleaned_data.get('crop')
        if not crop:
            raise forms.ValidationError("The crop field is mandatory.")
        return crop


class TreatmentOutcomeForm(forms.ModelForm):
    class Meta:
        model = TreatmentOutcome
        fields = ['pest', 'crop', 'treatment_method', 'date_applied', 'time_applied', 'effectiveness', 'notes']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()}),  # Set max to today's date
            'time_applied': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the crop field is marked as required
        self.fields['crop'].required = True

    def clean_date_applied(self):
        applied_date = self.cleaned_data['date_applied']
        if applied_date > date.today():
            raise ValidationError("The date applied cannot be in the future.")
        return applied_date
    
class ExpertResponseForm(forms.ModelForm):
    class Meta:
        model = PestSighting
        fields = ['pest_name', 'identification_confirmation', 'symptoms_recap', 'control_measures', 'next_steps', 'educational_nugget']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True  # Make all fields mandatory except the educational nugget

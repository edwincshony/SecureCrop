from django import forms
from django.core.exceptions import ValidationError
from .models import PestSighting, TreatmentOutcome
from pest_weed_db.models import Pest, Crop
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
    pest_name = forms.CharField(required=False, widget=forms.HiddenInput())  # Hidden field for custom pest name

    class Meta:
        model = TreatmentOutcome
        fields = ['pest', 'crop', 'treatment_method', 'date_applied', 'time_applied', 'effectiveness', 'notes']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date', 'max': date.today().isoformat()}),
            'time_applied': forms.TimeInput(attrs={'type': 'time', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['crop'].required = True
        self.fields['pest'].required = True

        # If pest_name is provided but no pest object matches (for creation)
        if 'pest_name' in kwargs.get('initial', {}) and not self.initial.get('pest'):
            pest_name = kwargs['initial']['pest_name']
            # Auto-create Pest with default values for required fields
            pest, created = Pest.objects.get_or_create(
                name=pest_name,
                defaults={
                    'description': 'Description pending update by expert.',
                    'symptoms': 'Symptoms pending update by expert.',
                    'control_measures': 'Control measures pending update by expert.',
                }
            )
            self.initial['pest'] = pest
            self.fields['pest'].initial = pest

        # Handle pre-filled crop and pest (for both create and update scenarios)
        crop_value = self.initial.get('crop')
        pest_value = self.initial.get('pest')

        # If an instance is being edited, initial might contain IDs instead of objects
        if self.instance and self.instance.pk:
            if not crop_value:  # If initial['crop'] is not set, use the instance's crop
                crop_value = self.instance.crop
                self.initial['crop'] = crop_value
            if not pest_value:  # If initial['pest'] is not set, use the instance's pest
                pest_value = self.instance.pest
                self.initial['pest'] = pest_value

        # Now handle the display of crop and pest (whether they're objects or IDs)
        if crop_value:
            # If crop_value is an ID (integer), fetch the object
            if isinstance(crop_value, int):
                try:
                    crop_value = Crop.objects.get(id=crop_value)
                    self.initial['crop'] = crop_value
                except Crop.DoesNotExist:
                    crop_value = None

            if crop_value:  # If we have a Crop object
                self.fields['crop'].widget.attrs.update({
                    'readonly': 'readonly',
                    'disabled': 'disabled',
                    'class': 'form-control',
                })
                # Set the display value for the dropdown
                self.fields['crop'].choices = [(crop_value.id, str(crop_value))] + list(self.fields['crop'].choices)
                self.fields['crop'].initial = crop_value.id

        if pest_value:
            # If pest_value is an ID (integer), fetch the object
            if isinstance(pest_value, int):
                try:
                    pest_value = Pest.objects.get(id=pest_value)
                    self.initial['pest'] = pest_value
                except Pest.DoesNotExist:
                    pest_value = None

            if pest_value:  # If we have a Pest object
                self.fields['pest'].widget.attrs.update({
                    'readonly': 'readonly',
                    'disabled': 'disabled',
                    'class': 'form-control',
                })
                # Set the display value for the dropdown
                self.fields['pest'].choices = [(pest_value.id, str(pest_value))] + list(self.fields['pest'].choices)
                self.fields['pest'].initial = pest_value.id

    def clean_date_applied(self):
        applied_date = self.cleaned_data['date_applied']
        if applied_date > date.today():
            raise ValidationError("The date applied cannot be in the future.")
        return applied_date

    def clean(self):
        cleaned_data = super().clean()
        pest = cleaned_data.get('pest')
        pest_name = self.initial.get('pest_name')

        # If no pest but pest_name exists, it should already be handled in __init__
        if not pest and pest_name:
            pest, created = Pest.objects.get_or_create(
                name=pest_name,
                defaults={
                    'description': 'Description pending update by expert.',
                    'symptoms': 'Symptoms pending update by expert.',
                    'control_measures': 'Control measures pending update by expert.',
                }
            )
            cleaned_data['pest'] = pest

        return cleaned_data

class ExpertResponseForm(forms.ModelForm):
    class Meta:
        model = PestSighting
        fields = ['pest_name', 'identification_confirmation', 'symptoms_recap', 'control_measures', 'next_steps', 'educational_nugget']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'educational_nugget':  # Educational nugget is optional
                self.fields[field].required = True
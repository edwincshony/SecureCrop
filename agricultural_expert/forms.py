from django import forms
from pest_weed_db.models import Pest, Weed

class PestForm(forms.ModelForm):
    class Meta:
        model = Pest
        fields = ['name', 'scientific_name', 'description', 'symptoms', 'control_measures', 'image']

class WeedForm(forms.ModelForm):
    class Meta:
        model = Weed
        fields = ['name', 'scientific_name', 'description', 'symptoms', 'control_measures', 'image']
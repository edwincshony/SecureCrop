from django import forms
from pest_weed_db.models import Pest, Weed,Crop

class PestForm(forms.ModelForm):
    class Meta:
        model = Pest
        fields = ['name', 'scientific_name', 'description', 'symptoms', 'control_measures', 'image']

class WeedForm(forms.ModelForm):
    class Meta:
        model = Weed
        fields = ['name', 'scientific_name', 'description', 'symptoms', 'control_measures', 'image']

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'species', 'description', 'growing_conditions', 'common_diseases', 'best_practices', 'image']

    def __init__(self, *args, **kwargs):
        super(CropForm, self).__init__(*args, **kwargs)
        # Make all fields mandatory
        for field_name in self.fields:
            self.fields[field_name].required = True

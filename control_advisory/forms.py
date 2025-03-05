from django import forms
from .models import AdvisoryRequest
from pest_weed_db.models import Crop

class AdvisoryForm(forms.ModelForm):
    # Dynamically populate crop_type choices from the Crop model
    crop_type = forms.ModelChoiceField(
        queryset=Crop.objects.all(),
        label="Crop Type",
        empty_label="--------"
    )

    class Meta:
        model = AdvisoryRequest
        fields = ['crop_type', 'location', 'issue_type', 'description']
        widgets = {
            'description': forms.Textarea,
        }
        labels = {
            'location': 'Location',
            'issue_type': 'Issue Type',
            'description': 'Description of Issue',
        }

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = AdvisoryRequest
        fields = ['recommendation']
        widgets = {
            'recommendation': forms.Textarea,
        }
        labels = {
            'recommendation': 'Recommendation',
        }
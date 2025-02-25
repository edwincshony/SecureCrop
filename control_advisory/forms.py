from django import forms
from .models import AdvisoryRequest

class AdvisoryForm(forms.ModelForm):
    class Meta:
        model = AdvisoryRequest
        fields = ['crop_type', 'location', 'issue_type', 'description']
        widgets = {
            'description': forms.Textarea,
        }
        labels = {
            'crop_type': 'Crop Type',
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
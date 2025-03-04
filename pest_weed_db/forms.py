from django import forms
from .models import CropLifecycle
from django.utils import timezone

class CropLifecycleForm(forms.ModelForm):
    class Meta:
        model = CropLifecycle
        fields = ['crop', 'stage', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'max': timezone.now().date().isoformat(),  # Sets max date to today
            }),
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator
from .models import CustomUser, FarmerProfile, ExpertProfile

class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
        help_text=""
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        help_text=""
    )
    phone_number = forms.CharField(
        required=False,
        max_length=10,
        validators=[MinLengthValidator(10)],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
        help_text="Phone number must be exactly 10 digits if provided."
    )
    first_name = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter you firstname'}),
        help_text=""
    )
    last_name = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter you lastname'}),
        help_text=""
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,  # Assuming ROLE_CHOICES is defined in your CustomUser model
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select your role"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
        help_text="",
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        help_text="",
        label="Password Confirmation"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', 'role', 'phone_number']

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['location', 'crop_types', 'profile_picture']

class ExpertProfileForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['expertise', 'experience_years', 'profile_picture']
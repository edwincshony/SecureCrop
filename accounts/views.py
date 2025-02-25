from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignupForm, FarmerProfileForm, ExpertProfileForm
from django import forms
from .models import CustomUser

# Form for CustomUser fields
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return render(request, 'accounts/signup_success.html')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Your login template

    def get_success_url(self):
        user = self.request.user
        print(f"User authenticated: {user.username}")  # Debug
        print(f"User role: {user.role}")  # Debug
        
        # Redirect based on user role
        if user.role == 'farmer':
            print("Redirecting farmer to dashboard")
            return '/farmer_dashboard/'
        elif user.role == 'agricultural_expert':
            print("Redirecting expert to expert_dashboard")
            return '/expert_dashboard/'
        elif user.role == 'admin':
            print("Redirecting admin to admin_dashboard")
            return '/admin_dashboard/'
        else:
            print("Redirecting to profile (default)")
            return '/profile/'

    def form_invalid(self, form):
        # Add error message for invalid login attempts
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

@login_required
def profile(request):
    user = request.user
    if user.role == 'farmer':
        profile = user.farmer_profile
        profile_form_class = FarmerProfileForm
    elif user.role == 'agricultural_expert':
        profile = user.expert_profile
        profile_form_class = ExpertProfileForm
    else:
        return render(request, 'accounts/profile.html', {'user': user})

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        profile_form = profile_form_class(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = CustomUserForm(instance=user)
        profile_form = profile_form_class(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form
    })

def logout_view(request):
    logout(request)
    return redirect('/login/')


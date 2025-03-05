from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from reports.models import PestSighting, TreatmentOutcome
from pest_weed_db.models import CropLifecycle
from control_advisory.models import AdvisoryRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import SignupForm, FarmerProfileForm, ExpertProfileForm
from django import forms
from .models import CustomUser
from admin_dash.models import UserApproval
from django.urls import reverse  # Add this import

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
            messages.success(request, "Account created. Awaiting admin approval.")
            return render(request, 'accounts/signup_success.html')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_superuser:
            try:
                approval = UserApproval.objects.get(user=user)
                if approval.status != 'approved':
                    messages.error(self.request, "Your account is pending approval or has been rejected.")
                    return self.form_invalid(form)
            except UserApproval.DoesNotExist:
                messages.error(self.request, "No approval record found. Contact an admin.")
                return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse('admin_dashboard')  # Use URL name instead of hardcoding
        elif user.role == 'farmer':
            return reverse('farmer_dashboard')
        elif user.role == 'agricultural_expert':
            return reverse('expert_dashboard')
        else:
            return reverse('profile')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username, password, or account status.')
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

@login_required
def public_profile(request, username):
    profile_owner = get_object_or_404(CustomUser, username=username)

    # Get farmer profile-related data
    pest_sightings = PestSighting.objects.filter(user=profile_owner)
    treatment_outcomes = TreatmentOutcome.objects.filter(user=profile_owner)
    advisory_requests = AdvisoryRequest.objects.filter(user=profile_owner)
    crop_lifecycle_events = CropLifecycle.objects.filter(user=profile_owner)

    context = {
        'profile_owner': profile_owner,
        'pest_sightings': pest_sightings,
        'treatment_outcomes': treatment_outcomes,
        'advisory_requests': advisory_requests,
        'crop_lifecycle_events': crop_lifecycle_events,
    }
    return render(request, 'accounts/public_profile.html', context)


def user_list(request):
    # Get only approved users: is_active=True and userapproval.status='approved'
    users = CustomUser.objects.filter(
        is_active=True,
        userapproval__status='approved'
    ).order_by('username')
    
    # Get the role filter from the query string (e.g., ?role=farmer)
    role_filter = request.GET.get('role', '')
    if role_filter in ['farmer', 'agricultural_expert']:
        users = users.filter(role=role_filter)

    context = {
        'users': users,
        'selected_role': role_filter,  # To highlight the active filter
    }
    return render(request, 'accounts/user_list.html', context)



def dashboard_overview(request):
    context = {
        "pest_sighting_count": PestSighting.objects.count(),
        "recent_pest_sighting": PestSighting.objects.order_by('-date').first(),
        
        "treatment_count": TreatmentOutcome.objects.count(),
        "recent_treatment": TreatmentOutcome.objects.order_by('-date_applied').first(),
        
        "advisory_request_count": AdvisoryRequest.objects.count(),
        "pending_advisories": AdvisoryRequest.objects.filter(status='pending').count(),
        
        "crop_event_count": CropLifecycle.objects.count(),
        "recent_crop_event": CropLifecycle.objects.order_by('-date').first(),
    }
    return render(request, "accounts/overview.html", context)

def pest_sightings_list(request):
    sightings = PestSighting.objects.order_by('-date')
    return render(request, "accounts/pest_sightings.html", {"sightings": sightings})

def treatments_list(request):
    treatments = TreatmentOutcome.objects.order_by('-date_applied')
    return render(request, "accounts/treatments.html", {"treatments": treatments})

def advisory_requests_list(request):
    advisory_requests = AdvisoryRequest.objects.all().order_by('-created_at')
    return render(request, "accounts/advisory_requests.html", {"requests": advisory_requests})

def crop_lifecycle_list1(request):
    events = CropLifecycle.objects.order_by('-date')
    return render(request, "accounts/crop_lifecycle.html", {"events": events})



def logout_view(request):
    logout(request)
    return redirect('/login/')
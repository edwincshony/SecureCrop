from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from control_advisory.models import AdvisoryRequest
from django.views.generic.edit import UpdateView, DeleteView
from control_advisory.forms import AdvisoryForm, RecommendationForm
from django.contrib import messages
from control_advisory.models import AdvisoryResponse
from accounts.models import CustomUser
from notifications.models import Notification
from reports.models import PestSighting, TreatmentOutcome
from django.core.exceptions import PermissionDenied
from pest_weed_db.models import Pest, Weed
from .forms import PestForm, WeedForm

# Role check mixin for experts
class ExpertRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Allow both superusers and agricultural experts
        return self.request.user.is_authenticated and (
            self.request.user.is_superuser or getattr(self.request.user, 'role', None) == 'agricultural_expert'
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        raise PermissionDenied  # Raise 403 if authenticated but lacks permissions

@login_required
def expert_dashboard(request):
    if request.user.role != 'agricultural_expert':
        messages.error(request, "Only agricultural experts can access this dashboard.")
        return redirect('login')

    # Fetch data for the dashboard
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    sightings = PestSighting.objects.all().order_by('-date')[:5]
    treatments = TreatmentOutcome.objects.all().order_by('-date_applied')[:5]
    advisory_requests = AdvisoryRequest.objects.filter(status='pending').order_by('-created_at')[:5]
    context = {
        'notifications': notifications,
        'sightings': sightings,
        'treatments': treatments,
        'advisory_requests': advisory_requests,
    }
    return render(request, 'agricultural_expert/dashboard.html', context)

@login_required
def all_advisory_requests(request):
    if request.user.role != 'agricultural_expert':
        messages.error(request, "Only agricultural experts can access this page.")
        return redirect('login')

    # Fetch all advisory requests (not just pending)
    advisory_requests = AdvisoryRequest.objects.all().order_by('-created_at')
    context = {
        'advisory_requests': advisory_requests,
    }
    return render(request, 'agricultural_expert/all_advisory_requests.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from control_advisory.models import AdvisoryRequest
from django.views.generic.edit import UpdateView, DeleteView
from control_advisory.forms import AdvisoryForm, RecommendationForm
from django.contrib import messages
from accounts.models import CustomUser
from notifications.models import Notification
from reports.models import PestSighting, TreatmentOutcome
from django.core.exceptions import PermissionDenied
from pest_weed_db.models import Pest, Weed
from .forms import PestForm, WeedForm

# Role check mixin for experts
class ExpertRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Allow both superusers and agricultural experts
        return self.request.user.is_authenticated and (
            self.request.user.is_superuser or getattr(self.request.user, 'role', None) == 'agricultural_expert'
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        raise PermissionDenied  # Raise 403 if authenticated but lacks permissions

@login_required
def expert_dashboard(request):
    if request.user.role != 'agricultural_expert':
        messages.error(request, "Only agricultural experts can access this dashboard.")
        return redirect('login')

    # Fetch data for the dashboard
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    sightings = PestSighting.objects.all().order_by('-date')[:5]
    treatments = TreatmentOutcome.objects.all().order_by('-date_applied')[:5]
    advisory_requests = AdvisoryRequest.objects.filter(status='pending').order_by('-created_at')[:5]
    context = {
        'notifications': notifications,
        'sightings': sightings,
        'treatments': treatments,
        'advisory_requests': advisory_requests,
    }
    return render(request, 'agricultural_expert/dashboard.html', context)

@login_required
def all_advisory_requests(request):
    if request.user.role != 'agricultural_expert':
        messages.error(request, "Only agricultural experts can access this page.")
        return redirect('login')

    # Fetch all advisory requests (not just pending)
    advisory_requests = AdvisoryRequest.objects.all().order_by('-created_at')
    context = {
        'advisory_requests': advisory_requests,
    }
    return render(request, 'agricultural_expert/all_advisory_requests.html', context)

@login_required
def respond_advisory(request, pk):
    if request.user.role != 'agricultural_expert':
        return redirect('login')
    
    advisory_request = get_object_or_404(AdvisoryRequest, pk=pk)

    if request.method == 'POST':
        form = RecommendationForm(request.POST, instance=advisory_request)
        if form.is_valid():
            advisory_request = form.save(commit=False)
            if advisory_request.status == 'pending':
                advisory_request.status = 'responded'
            advisory_request.responded_by = request.user
            advisory_request.save()
            AdvisoryResponse.objects.create(
                advisory_request=advisory_request,
                expert=request.user,
                response_text=advisory_request.recommendation
            )
            messages.success(request, "Recommendation sent to the farmer.")
            return redirect('expert_dashboard')
    else:
        form = RecommendationForm(instance=advisory_request)

    return render(request, 'agricultural_expert/respond_advisory.html', {
        'form': form,
        'advisory_request': advisory_request,
    })



@login_required
def manage_database(request):
    # Check user role
    if request.user.role not in ['agricultural_expert', 'farmer']:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login')

    # Determine if the user is an expert (for edit/add/delete permissions)
    is_expert = request.user.role == 'agricultural_expert'

    # Pass context to the template
    context = {
        'is_expert': is_expert,
        # Add your pest/weed data here, e.g., Pest.objects.all() if you have a Pest model
    }
    return render(request, 'agricultural_expert/manage_database.html', context)


@login_required
def manage_database(request):
    # Check user role
    if request.user.role not in ['agricultural_expert', 'farmer']:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('login')

    # Determine if the user is an expert (for edit/add/delete permissions)
    is_expert = request.user.role == 'agricultural_expert'

    # Pass context to the template
    context = {
        'is_expert': is_expert,
        # Add your pest/weed data here, e.g., Pest.objects.all() if you have a Pest model
    }
    return render(request, 'agricultural_expert/manage_database.html', context)

@login_required
def advisory_response_history(request, pk):
    advisory_request = get_object_or_404(AdvisoryRequest, pk=pk)
    responses = advisory_request.responses.all().order_by('-created_at')  # Newest first
    
    context = {
        'advisory_request': advisory_request,
        'responses': responses,
    }
    return render(request, 'agricultural_expert/response_history.html', context)



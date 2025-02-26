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
        # Check if user is authenticated and has the 'agricultural_expert' role
        return self.request.user.is_authenticated and getattr(self.request.user, 'role', None) == 'agricultural_expert'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        raise PermissionDenied  # Raise 403 if authenticated but wrong role

@login_required
def expert_dashboard(request):
    if request.user.role != 'agricultural_expert':
        messages.error(request, "Only agricultural experts can access this dashboard.")
        return redirect('accounts:login')

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
        return redirect('accounts:login')

    # Fetch all pending advisory requests
    advisory_requests = AdvisoryRequest.objects.filter(status='pending').order_by('-created_at')
    context = {
        'advisory_requests': advisory_requests,
    }
    return render(request, 'agricultural_expert/all_advisory_requests.html', context)

@login_required
def respond_advisory(request, pk):
    if request.user.role != 'agricultural_expert':
        return redirect('accounts:login')
    advisory_request = get_object_or_404(AdvisoryRequest, pk=pk, status='pending')
    if request.method == 'POST':
        form = RecommendationForm(request.POST, instance=advisory_request)
        if form.is_valid():
            advisory_request = form.save(commit=False)
            advisory_request.status = 'responded'
            advisory_request.responded_by = request.user
            advisory_request.save()
            # Notify the farmer
            Notification.objects.create(
                user=advisory_request.user,
                title=f"Recommendation for {advisory_request.crop_type}",
                message=f"An expert has provided a recommendation for your {advisory_request.issue_type} issue.",
                url=f"/farmer/advisory-responses/"
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
    if request.user.role != 'agricultural_expert':
        messages.error(request, "Only agricultural experts can access this page.")
        return redirect('accounts:login')
    return render(request, 'agricultural_expert/manage_database.html')
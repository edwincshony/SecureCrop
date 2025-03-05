from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pest_weed_db.models import Pest, Weed
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from accounts.models import CustomUser
from control_advisory.models import AdvisoryRequest, AdvisoryResponse
from notifications.models import Notification
from control_advisory.models import AdvisoryRequest
from reports.models import PestSighting, TreatmentOutcome
from control_advisory.forms import AdvisoryForm
from django.contrib import messages

# Role check mixin for farmers
class FarmerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'farmer'

@login_required
def farmer_dashboard(request):
    if request.user.role != 'farmer':
        messages.error(request, "Only farmers can access this dashboard.")
        return redirect('login')

    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    sightings = PestSighting.objects.filter(user=request.user).order_by('-date')[:5]
    treatments = TreatmentOutcome.objects.filter(user=request.user).order_by('-date_applied')[:5]
    advisory_requests = AdvisoryRequest.objects.filter(user=request.user).order_by('-created_at')[:5]

    if request.method == 'POST' and 'advisory_submit' in request.POST:
        advisory_form = AdvisoryForm(request.POST)
        if advisory_form.is_valid():
            advisory_request = advisory_form.save(commit=False)
            advisory_request.user = request.user
            advisory_request.status = 'pending'
            advisory_request.save()
            return render(request, 'farmer/advisory_success.html', {'advisory_request': advisory_request})
    else:
        advisory_form = AdvisoryForm()

    context = {
        'notifications': notifications,
        'sightings': sightings,
        'treatments': treatments,
        'advisory_requests': advisory_requests,
        'advisory_form': advisory_form,
    }
    return render(request, 'farmer/dashboard.html', context)

@login_required
def advisory_responses(request):
    if request.user.role != 'farmer':
        return redirect('login')
    advisory_requests = AdvisoryRequest.objects.filter(user=request.user, status='responded').order_by('-updated_at')
    return render(request, 'farmer/advisory_responses.html', {'advisory_requests': advisory_requests})

class PestSightingDeleteView(LoginRequiredMixin, FarmerRequiredMixin, DeleteView):
    model = PestSighting
    template_name = 'farmer/confirm_delete.html'
    success_url = '/farmer/dashboard/'
    def get_queryset(self):
        return PestSighting.objects.filter(user=self.request.user)

class TreatmentOutcomeDeleteView(LoginRequiredMixin, FarmerRequiredMixin, DeleteView):
    model = TreatmentOutcome
    template_name = 'farmer/confirm_delete.html'
    success_url = '/farmer/dashboard/'
    def get_queryset(self):
        return TreatmentOutcome.objects.filter(user=self.request.user)
    

@login_required
def advisory_requests_page(request):
    # Handle form submission
    if request.method == 'POST':
        form = AdvisoryForm(request.POST)
        if form.is_valid():
            advisory_request = form.save(commit=False)
            advisory_request.user = request.user  # Associate the request with the logged-in user
            advisory_request.status = 'pending'
            advisory_request.save()
            return redirect('advisory_requests_page')  # Redirect to the same page after submission
    else:
        form = AdvisoryForm()

    # Fetch recent advisory requests for the logged-in user
    advisory_requests = AdvisoryRequest.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'advisory_form': form,
        'advisory_requests': advisory_requests,
    }
    return render(request, 'farmer/advisory_requests.html', context)

@login_required
def advisory_request_detail(request, request_id):
    advisory_request = get_object_or_404(AdvisoryRequest, id=request_id, user=request.user)

    responses = AdvisoryResponse.objects.filter(advisory_request=advisory_request).order_by('-created_at')

    
    context = {
        'advisory_request': advisory_request,
        'responses': responses
    }
    return render(request, 'farmer/advisory_request_detail.html', context)





@login_required
def edit_advisory_request(request, pk):
    advisory_request = get_object_or_404(AdvisoryRequest, id=pk, user=request.user)
    
    

    if request.method == 'POST':
        form = AdvisoryForm(request.POST, instance=advisory_request)
        if form.is_valid():
            form.save()
            messages.success(request, "Your advisory request has been updated successfully.")
            return redirect('advisory_requests_page')
    else:
        form = AdvisoryForm(instance=advisory_request)

    context = {
        'form': form,
        'advisory_request': advisory_request,
    }
    return render(request, 'farmer/edit_advisory_request.html', context)


@login_required
def delete_advisory_request(request, pk):
    """
    View to handle the deletion of an advisory request.
    Only pending requests can be deleted.
    """
    # Fetch the advisory request by ID and ensure it belongs to the logged-in user
    advisory_request = get_object_or_404(AdvisoryRequest, id=pk, user=request.user)
    
 
    # Handle POST request for deletion
    if request.method == 'POST':
        advisory_request.delete()  # Delete the advisory request from the database
        messages.success(request, "Your advisory request has been deleted successfully.")
        return redirect('advisory_requests_page')  # Redirect to the advisory requests page

    # Render the confirmation page for GET requests
    context = {
        'advisory_request': advisory_request,
    }
    return render(request, 'farmer/confirm_delete.html', context)
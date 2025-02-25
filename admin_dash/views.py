from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.contrib import messages
from django.db.models import Q
from control_advisory.models import AdvisoryRequest
from accounts.models import CustomUser
from pest_weed_db.models import Pest, Weed
from notifications.models import Notification
from reports.models import PestSighting, TreatmentOutcome
from .models import UserApproval

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access this dashboard.")
        return redirect('accounts:login')

    # Search functionality
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(~Q(is_superuser=True))  # Exclude admins
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )

    pest_sightings = PestSighting.objects.all().order_by('-date')[:5]
    treatments = TreatmentOutcome.objects.all().order_by('-date_applied')[:5]
    advisory_requests = AdvisoryRequest.objects.all().order_by('-created_at')[:5]
    pests = Pest.objects.all().count()
    weeds = Weed.objects.all().count()

    context = {
        'users': users,
        'query': query,
        'pest_sightings': pest_sightings,
        'treatments': treatments,
        'advisory_requests': advisory_requests,
        'pests': pests,
        'weeds': weeds,
    }
    return render(request, 'admin_dash/dashboard.html', context)

@login_required
def approve_user(request, pk):
    if not request.user.is_superuser:
        return redirect('accounts:login')
    approval = get_object_or_404(UserApproval, pk=pk)
    if request.method == 'POST':
        approval.status = 'approved'
        approval.user.is_active = True  # Activate user
        approval.user.save()
        approval.save()
        messages.success(request, f"User {approval.user.username} approved.")
        return redirect('admin_dashboard')
    return render(request, 'admin_dash/confirm_action.html', {'action': 'approve', 'user': approval.user})

@login_required
def reject_user(request, pk):
    if not request.user.is_superuser:
        return redirect('accounts:login')
    approval = get_object_or_404(UserApproval, pk=pk)
    if request.method == 'POST':
        approval.status = 'rejected'
        approval.save()
        messages.success(request, f"User {approval.user.username} rejected.")
        return redirect('admin_dashboard')
    return render(request, 'admin_dash/confirm_action.html', {'action': 'reject', 'user': approval.user})

@login_required
def view_profile(request, pk):
    if not request.user.is_superuser:
        return redirect('accounts:login')
    user = get_object_or_404(CustomUser, pk=pk)
    profile = user.farmer_profile if user.role == 'farmer' else user.expert_profile if user.role == 'agricultural_expert' else None
    return render(request, 'admin_dash/view_profile.html', {'user': user, 'profile': profile})

class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'admin_dash/confirm_delete.html'
    success_url = '/admin_dash/dashboard/'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if hasattr(user, 'notifications'):
            user.notifications.all().delete()  # Clean up notifications
        if hasattr(user, 'farmer_profile') or hasattr(user, 'expert_profile'):
            user.farmer_profile.delete() if user.role == 'farmer' else user.expert_profile.delete() if user.role == 'agricultural_expert' else None
        if hasattr(user, 'userapproval'):
            user.userapproval.delete()
        return super().delete(request, *args, **kwargs)

class PestSightingDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = PestSighting
    template_name = 'admin_dash/confirm_delete.html'
    success_url = '/admin_dash/dashboard/'

class TreatmentOutcomeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TreatmentOutcome
    template_name = 'admin_dash/confirm_delete.html'
    success_url = '/admin_dash/dashboard/'
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from accounts.models import FarmerProfile, ExpertProfile  # Import profile models
from django.contrib import messages
from django.db.models import Q
from control_advisory.models import AdvisoryRequest
from accounts.models import CustomUser
from pest_weed_db.models import Pest, Weed
from notifications.models import Notification
from reports.models import PestSighting, TreatmentOutcome
from .models import UserApproval
from accounts.forms import SignupForm

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access this dashboard.")
        return redirect('accounts:login')

    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(~Q(is_superuser=True))
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
        approval.user.is_active = True
        approval.user.save()
        approval.save()
        messages.success(request, f"User {approval.user.username} approved.")
        return redirect('admin_user_management')
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
        return redirect('admin_user_management')
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
    success_url = '/admin_dash/admin/users/'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if hasattr(user, 'notifications'):
            user.notifications.all().delete()
        if hasattr(user, 'farmer_profile') or hasattr(user, 'expert_profile'):
            user.farmer_profile.delete() if user.role == 'farmer' else user.expert_profile.delete() if user.role == 'agricultural_expert' else None
        if hasattr(user, 'userapproval'):
            user.userapproval.delete()
        messages.success(request, f"User {user.username} deleted.")
        return super().delete(request, *args, **kwargs)

@login_required
def admin_user_management(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('accounts:login')

    query = request.GET.get('q', '')
    # Filter for approved users only:
    # 1. Admin-registered users (admin_registered=True)
    # 2. Self-signup users with UserApproval status 'approved'
    users = CustomUser.objects.filter(
        ~Q(is_superuser=True) & (
            Q(admin_registered=True) | 
            Q(userapproval__status='approved')
        )
    ).order_by('username')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )

    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'admin_dash/user_management.html', context)

@login_required
def register_user(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('accounts:login')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Active immediately
            user.admin_registered = True  # Flag as admin-registered
            user.save()
            
            # Create profile
            if user.role == 'farmer':
                FarmerProfile.objects.get_or_create(user=user)
            elif user.role == 'agricultural_expert':
                ExpertProfile.objects.get_or_create(user=user)

            messages.success(request, f"User {user.username} registered successfully.")
            return redirect('admin_user_management')
    else:
        form = SignupForm()

    return render(request, 'admin_dash/register_user.html', {'form': form})

@login_required
def pending_approvals(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('accounts:login')

    query = request.GET.get('q', '')
    pending_approvals = UserApproval.objects.filter(status='pending').order_by('user__username')
    
    if query:
        pending_approvals = pending_approvals.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__role__icontains=query)
        )

    return render(request, 'admin_dash/pending_users.html', {'pending_approvals': pending_approvals, 'query': query})

@login_required
def admin_advisory_requests(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('accounts:login')
    advisory_requests = AdvisoryRequest.objects.all().order_by('-created_at')
    return render(request, 'admin_dash/advisory_requests.html', {'advisory_requests': advisory_requests})

@login_required
def admin_pest_sightings(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('accounts:login')
    pest_sightings = PestSighting.objects.all().order_by('-date')
    return render(request, 'admin_dash/pest_sightings.html', {'pest_sightings': pest_sightings})

@login_required
def admin_treatment_outcomes(request):
    if not request.user.is_superuser:
        messages.error(request, "Unauthorized access.")
        return redirect('accounts:login')
    treatments = TreatmentOutcome.objects.all().order_by('-date_applied')
    return render(request, 'admin_dash/treatment_outcomes.html', {'treatments': treatments})

class AdvisoryRequestDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = AdvisoryRequest
    success_url = '/admin_dash/admin/advisory/'


class PestSightingDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = PestSighting
    template_name = 'admin_dash/confirm_delete.html'
    success_url = '/admin_dash/dashboard/'

class TreatmentOutcomeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = TreatmentOutcome
    template_name = 'admin_dash/confirm_delete.html'
    success_url = '/admin_dash/dashboard/'


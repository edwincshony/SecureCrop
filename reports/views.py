from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import PestSighting, TreatmentOutcome
from pest_weed_db.models import Crop, Pest
from .forms import PestSightingForm, TreatmentOutcomeForm, ExpertResponseForm  # Correct import
from django.urls import reverse_lazy
from django.contrib import messages

class PestSightingCreateView(LoginRequiredMixin, CreateView):
    model = PestSighting
    form_class = PestSightingForm
    template_name = 'reports/pest_sighting_form.html'
    success_url = reverse_lazy('pest_infestations')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import PestSighting, TreatmentOutcome
from pest_weed_db.models import Crop, Pest
from .forms import PestSightingForm, TreatmentOutcomeForm, ExpertResponseForm
from django.urls import reverse_lazy
from django.contrib import messages

class TreatmentOutcomeCreateView(LoginRequiredMixin, CreateView):
    model = TreatmentOutcome
    form_class = TreatmentOutcomeForm
    template_name = 'reports/treatment_outcome_form.html'
    success_url = reverse_lazy('treatment_outcomes')

    def get_initial(self):
        initial = super().get_initial()
        crop_id = self.kwargs.get('crop_id')
        pest_name = self.kwargs.get('pest_name')

        if crop_id:
            try:
                crop = Crop.objects.get(id=crop_id)
                initial['crop'] = crop
            except Crop.DoesNotExist:
                initial['crop'] = None

        if pest_name:
            initial['pest_name'] = pest_name
            try:
                pest = Pest.objects.get(name=pest_name)
                initial['pest'] = pest
            except Pest.DoesNotExist:
                initial['pest'] = None  # Form will handle creation

        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PestInfestationsReportView(LoginRequiredMixin, ListView):
    model = PestSighting
    template_name = 'reports/pest_infestations.html'
    context_object_name = 'sightings'

    def get_queryset(self):
        user = self.request.user
        queryset = PestSighting.objects.all().order_by('-date', '-time')
        
        if user.role == 'farmer':
            queryset = PestSighting.objects.filter(user=user).order_by('-date', '-time')
            
        crop_id = self.request.GET.get('crop')
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crops'] = Crop.objects.all()
        context['selected_crop'] = self.request.GET.get('crop', '')
        return context

class TreatmentOutcomesReportView(LoginRequiredMixin, ListView):
    model = TreatmentOutcome
    template_name = 'reports/treatment_outcomes.html'
    context_object_name = 'outcomes'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return TreatmentOutcome.objects.filter(user=user).order_by('-date_applied', '-time_applied')
        return TreatmentOutcome.objects.all().order_by('-date_applied', '-time_applied')

class PestSightingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PestSighting
    form_class = PestSightingForm
    template_name = 'reports/pest_sighting_form.html'
    success_url = reverse_lazy('pest_infestations')

    def test_func(self):
        sighting = self.get_object()
        return self.request.user == sighting.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to edit this report.")
        return redirect('pest_infestations')

class PestSightingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PestSighting
    success_url = reverse_lazy('pest_infestations')

    def test_func(self):
        sighting = self.get_object()
        return self.request.user == sighting.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to delete this report.")
        return redirect('pest_infestations')

class TreatmentOutcomeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TreatmentOutcome
    form_class = TreatmentOutcomeForm
    template_name = 'reports/treatment_outcome_form.html'
    success_url = reverse_lazy('treatment_outcomes')

    def test_func(self):
        outcome = self.get_object()
        return self.request.user == outcome.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to edit this report.")
        return redirect('treatment_outcomes')

class TreatmentOutcomeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TreatmentOutcome
    success_url = reverse_lazy('treatment_outcomes')

    def test_func(self):
        outcome = self.get_object()
        return self.request.user == outcome.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to delete this report.")
        return redirect('treatment_outcomes')

class ExpertResponseView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PestSighting
    form_class = ExpertResponseForm
    template_name = 'reports/expert_response_form.html'
    success_url = reverse_lazy('pest_infestations')

    def test_func(self):
        return self.request.user.role == 'agricultural_expert'

    def form_valid(self, form):
        pest_name = form.cleaned_data.get('pest_name')
        if pest_name:
            Pest.objects.get_or_create(
                name=pest_name,
                defaults={
                    'description': 'Description pending update by expert.',
                    'symptoms': 'Symptoms pending update by expert.',
                    'control_measures': 'Control measures pending update by expert.',
                }
            )
        form.instance.expert = self.request.user
        return super().form_valid(form)


class ExpertResponseDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = PestSighting
    template_name = 'reports/expert_response_detail.html'
    context_object_name = 'sighting'

    def test_func(self):
        sighting = self.get_object()
        return self.request.user == sighting.user or self.request.user.role == 'agricultural_expert'

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to view this response.")
        return redirect('pest_infestations')
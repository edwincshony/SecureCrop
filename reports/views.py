from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import PestSighting, TreatmentOutcome
from .forms import PestSightingForm, TreatmentOutcomeForm
from django.urls import reverse_lazy
from django.contrib import messages

class PestSightingCreateView(LoginRequiredMixin, CreateView):
    model = PestSighting
    form_class = PestSightingForm
    template_name = 'reports/pest_sighting_form.html'
    success_url = '/reports/pest-infestations/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TreatmentOutcomeCreateView(LoginRequiredMixin, CreateView):
    model = TreatmentOutcome
    form_class = TreatmentOutcomeForm
    template_name = 'reports/treatment_outcome_form.html'
    success_url = '/reports/treatment-outcomes/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PestInfestationsReportView(LoginRequiredMixin, ListView):
    model = PestSighting
    template_name = 'reports/pest_infestations.html'
    context_object_name = 'sightings'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return PestSighting.objects.filter(user=user).order_by('-date', '-time')
        return PestSighting.objects.all().order_by('-date', '-time')

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
    success_url = '/reports/pest-infestations/'

    def test_func(self):
        sighting = self.get_object()
        return self.request.user == sighting.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to edit this report.")
        return redirect('pest_infestations')

class PestSightingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PestSighting
    success_url = '/reports/pest-infestations/'

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
    success_url = '/reports/treatment-outcomes/'

    def test_func(self):
        outcome = self.get_object()
        return self.request.user == outcome.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to edit this report.")
        return redirect('treatment_outcomes')

class TreatmentOutcomeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TreatmentOutcome
    success_url = '/reports/treatment-outcomes/'

    def test_func(self):
        outcome = self.get_object()
        return self.request.user == outcome.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You don’t have permission to delete this report.")
        return redirect('treatment_outcomes')
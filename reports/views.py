from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PestSighting, TreatmentOutcome
from .forms import PestSightingForm, TreatmentOutcomeForm

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
        return PestSighting.objects.all().order_by('-date')

class TreatmentOutcomesReportView(LoginRequiredMixin, ListView):
    model = TreatmentOutcome
    template_name = 'reports/treatment_outcomes.html'
    context_object_name = 'outcomes'

    def get_queryset(self):
        return TreatmentOutcome.objects.all().order_by('-date_applied')
from django.urls import path
from .views import (
    PestSightingCreateView,
    TreatmentOutcomeCreateView,
    PestInfestationsReportView,
    TreatmentOutcomesReportView,
)

urlpatterns = [
    path('pest-sighting/', PestSightingCreateView.as_view(), name='pest_sighting_create'),
    path('treatment-outcome/', TreatmentOutcomeCreateView.as_view(), name='treatment_outcome_create'),
    path('pest-infestations/', PestInfestationsReportView.as_view(), name='pest_infestations'),
    path('treatment-outcomes/', TreatmentOutcomesReportView.as_view(), name='treatment_outcomes'),
]
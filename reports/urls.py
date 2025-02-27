from django.urls import path
from .views import (
    PestSightingCreateView,
    TreatmentOutcomeCreateView,
    PestInfestationsReportView,
    TreatmentOutcomesReportView,
    PestSightingUpdateView,
    PestSightingDeleteView,
    TreatmentOutcomeUpdateView,
    TreatmentOutcomeDeleteView,
)


urlpatterns = [
    path('pest-sighting/', PestSightingCreateView.as_view(), name='pest_sighting_create'),
    path('treatment-outcome/', TreatmentOutcomeCreateView.as_view(), name='treatment_outcome_create'),
    path('pest-infestations/', PestInfestationsReportView.as_view(), name='pest_infestations'),
    path('treatment-outcomes/', TreatmentOutcomesReportView.as_view(), name='treatment_outcomes'),
    path('pest-sighting/<int:pk>/edit/', PestSightingUpdateView.as_view(), name='pest_sighting_edit'),
    path('pest-sighting/<int:pk>/delete/', PestSightingDeleteView.as_view(), name='pest_sighting_delete'),
    path('treatment-outcome/<int:pk>/edit/', TreatmentOutcomeUpdateView.as_view(), name='treatment_outcome_edit'),
    path('treatment-outcome/<int:pk>/delete/', TreatmentOutcomeDeleteView.as_view(), name='treatment_outcome_delete'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('pest-infestations/', views.PestInfestationsReportView.as_view(), name='pest_infestations'),
    path('pest-sighting/add/', views.PestSightingCreateView.as_view(), name='pest_sighting_create'),
    path('pest-sighting/<int:pk>/edit/', views.PestSightingUpdateView.as_view(), name='pest_sighting_edit'),
    path('pest-sighting/<int:pk>/delete/', views.PestSightingDeleteView.as_view(), name='pest_sighting_delete'),
    path('treatment-outcome/add/', views.TreatmentOutcomeCreateView.as_view(), name='treatment_outcome_create'),
    path('treatment-outcome/add/crop/<int:crop_id>/pest/<str:pest_name>/', 
         views.TreatmentOutcomeCreateView.as_view(), 
         name='treatment_outcome_create_from_sighting'),
    path('treatment-outcomes/', views.TreatmentOutcomesReportView.as_view(), name='treatment_outcomes'),
    path('treatment-outcome/<int:pk>/edit/', views.TreatmentOutcomeUpdateView.as_view(), name='treatment_outcome_edit'),
    path('treatment-outcome/<int:pk>/delete/', views.TreatmentOutcomeDeleteView.as_view(), name='treatment_outcome_delete'),
    path('expert-response/<int:pk>/', views.ExpertResponseView.as_view(), name='expert_response'),
    path('expert-response-detail/<int:pk>/', views.ExpertResponseDetailView.as_view(), name='expert_response_detail'),
]
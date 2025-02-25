from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('dashboard/', farmer_dashboard, name='farmer_dashboard'),
    path('advisory-responses/', advisory_responses, name='advisory_responses'),
    path('sighting/<int:pk>/delete/', PestSightingDeleteView.as_view(), name='sighting_delete'),
    path('treatment/<int:pk>/delete/', TreatmentOutcomeDeleteView.as_view(), name='treatment_delete'),

    path('advisory-requests/', views.advisory_requests_page, name='advisory_requests_page'),
    path('advisory-requests/edit/<int:pk>/', edit_advisory_request, name='edit_advisory_request'),
    path('advisory-requests/delete/<int:pk>/', delete_advisory_request, name='delete_advisory_request'),
]
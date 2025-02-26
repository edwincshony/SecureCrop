from django.urls import path
from . import views
from .views import approve_user, reject_user, view_profile, UserDeleteView, PestSightingDeleteView, TreatmentOutcomeDeleteView, AdvisoryRequestDeleteView

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/<int:pk>/approve/', approve_user, name='approve_user'),
    path('user/<int:pk>/reject/', reject_user, name='reject_user'),
    path('user/<int:pk>/view/', view_profile, name='view_profile'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('sighting/<int:pk>/delete/', PestSightingDeleteView.as_view(), name='admin_sighting_delete'),
    path('treatment/<int:pk>/delete/', TreatmentOutcomeDeleteView.as_view(), name='admin_treatment_delete'),
    path('admin/users/', views.admin_user_management, name='admin_user_management'),
    path('admin/pending-approvals/', views.pending_approvals, name='pending_approvals'),
    path('admin/register-user/', views.register_user, name='register_user'),
    path('admin/advisory/', views.admin_advisory_requests, name='admin_advisory_requests'),
    path('admin/advisory/<int:pk>/delete/', AdvisoryRequestDeleteView.as_view(), name='admin_advisory_requests_delete'),
    path('admin/pests/', views.admin_pest_sightings, name='admin_pest_sightings'),
    path('admin/treatments/', views.admin_treatment_outcomes, name='admin_treatment_outcomes'),
]
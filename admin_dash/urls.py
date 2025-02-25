from django.urls import path
from . import views
from .views import approve_user, reject_user, view_profile, UserDeleteView, PestSightingDeleteView, TreatmentOutcomeDeleteView

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/<int:pk>/approve/', approve_user, name='approve_user'),
    path('user/<int:pk>/reject/', reject_user, name='reject_user'),
    path('user/<int:pk>/view/', view_profile, name='view_profile'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
    path('sighting/<int:pk>/delete/', PestSightingDeleteView.as_view(), name='admin_sighting_delete'),
    path('treatment/<int:pk>/delete/', TreatmentOutcomeDeleteView.as_view(), name='admin_treatment_delete'),
]
from django.urls import path
from .import views
from .views import expert_dashboard, PestCreateView, PestUpdateView, WeedCreateView, WeedUpdateView,respond_advisory

urlpatterns = [
    path('expert_dashboard/', expert_dashboard, name='expert_dashboard'),
    path('respond_advisory/<int:pk>/', views.respond_advisory, name='respond_advisory'),
    path('pest/add/', PestCreateView.as_view(), name='pest_add'),
    path('advisory-requests/', views.all_advisory_requests, name='all_advisory_requests'),  # New route
    path('weed/add/', WeedCreateView.as_view(), name='weed_add'),
    path('manage-database/', views.manage_database, name='manage_database'),

    path('pest/<int:pk>/edit/', PestUpdateView.as_view(), name='pest_edit'),
    path('weed/<int:pk>/edit/', WeedUpdateView.as_view(), name='weed_edit'),
    
]
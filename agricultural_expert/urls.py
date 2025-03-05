from django.urls import path
from .import views
from .views import expert_dashboard,respond_advisory

urlpatterns = [
    path('expert_dashboard/', expert_dashboard, name='expert_dashboard'),
    path('respond_advisory/<int:pk>/', views.respond_advisory, name='respond_advisory'),
    path('advisory-requests/', views.all_advisory_requests, name='all_advisory_requests'),  # New route
    path('manage-database/', views.manage_database, name='manage_database'),
    path('advisory/<int:pk>/responses/', views.advisory_response_history, name='advisory_response_history'),


   


    
]
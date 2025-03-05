from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),  # New URL
    path('users/', views.user_list, name='user_list'),  # New URL for user list
    path('overview/', views.dashboard_overview, name='dashboard_overview'),
    path("dashboard/pest-sightings/", views.pest_sightings_list, name="pest_sightings_list"),
    path("dashboard/treatments/", views.treatments_list, name="treatments_list"),
    path("dashboard/advisory-requests/", views.advisory_requests_list, name="advisory_requests_list"),
    path("dashboard/crop_lifecycle_list1/", views.crop_lifecycle_list1, name="crop_lifecycle_list1"),


]
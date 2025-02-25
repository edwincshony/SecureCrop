from django.urls import path
from . import views

urlpatterns = [
    path('advisory/', views.advisory, name='advisory'),
]
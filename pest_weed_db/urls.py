from django.urls import path
from . import views
from .views import PestCreateView, PestUpdateView, WeedCreateView, WeedUpdateView, PestDeleteView, WeedDeleteView


urlpatterns = [
    path('pests/', views.pest_list, name='pest_list'),
    path('pests/<int:pk>/', views.pest_detail, name='pest_detail'),
    path('weeds/', views.weed_list, name='weed_list'),
    path('weeds/<int:pk>/', views.weed_detail, name='weed_detail'),
    path('pest/<int:pk>/edit/', PestUpdateView.as_view(), name='pest_edit'),
    path('weed/<int:pk>/edit/', WeedUpdateView.as_view(), name='weed_edit'),
    path('pest/add/', PestCreateView.as_view(), name='pest_add'),
    path('weed/add/', WeedCreateView.as_view(), name='weed_add'),
    path('pest/<int:pk>/delete/', PestDeleteView.as_view(), name='pest_delete'),
    path('weed/<int:pk>/delete/', WeedDeleteView.as_view(), name='weed_delete'),
    path('crop_list/', views.crop_list, name='crop_list'),
    path('<int:pk>/', views.crop_detail, name='crop_detail'),
    path('create/', views.CropCreateView.as_view(), name='crop_create'),
    path('<int:pk>/update/', views.CropUpdateView.as_view(), name='crop_update'),
    path('<int:pk>/delete/', views.CropDeleteView.as_view(), name='crop_delete'),  # AJAX delete

    path('crop_lifecycle_list', views.CropLifecycleListView.as_view(), name='crop_lifecycle_list'),
    path('add/', views.CropLifecycleCreateView.as_view(), name='crop_lifecycle_create'),

    path('<int:pk>/edit/', views.CropLifecycleUpdateView.as_view(), name='crop_lifecycle_edit'),
    path('lifecycle/<int:pk>/delete/', views.CropLifecycleDeleteView.as_view(), name='crop_lifecycle_delete'),
]
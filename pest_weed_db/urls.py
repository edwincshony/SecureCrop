from django.urls import path
from . import views


urlpatterns = [
    path('pests/', views.pest_list, name='pest_list'),
    path('pests/<int:pk>/', views.pest_detail, name='pest_detail'),
    path('weeds/', views.weed_list, name='weed_list'),
    path('weeds/<int:pk>/', views.weed_detail, name='weed_detail'),

]
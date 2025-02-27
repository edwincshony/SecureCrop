"""
URL configuration for crop_guardian project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from agricultural_expert.views import expert_dashboard  # Import the view
from farmer.views import farmer_dashboard  # Import the view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('pest_weed_db.urls')),
    path('', include('control_advisory.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include('reports.urls')),
    path('farmer/', include('farmer.urls')),
    path('agricultural_expert/', include('agricultural_expert.urls')),
    path('admin_dash/', include('admin_dash.urls')),
    path('expert_dashboard/', expert_dashboard, name='expert_dashboard'),
    path('farmer_dashboard/', farmer_dashboard, name='farmer_dashboard'),
    path('messaging/', include('messaging.urls')),  # Add this line
    path('discussions/', include('discussions.urls')),  # Add this line





]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from agricultural_expert.views import expert_dashboard
from farmer.views import farmer_dashboard

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
    path('messaging/', include('messaging.urls')),
    path('discussions/', include('discussions.urls')),
]

# Serve media and static files (for Vercel and other production setups)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

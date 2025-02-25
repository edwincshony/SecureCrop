from django.urls import path
from .views import NotificationListView, mark_all_read

urlpatterns = [
    path('notification_list', NotificationListView.as_view(), name='notification_list'),
    path('mark_all_read/', mark_all_read, name='mark_all_read'),
]
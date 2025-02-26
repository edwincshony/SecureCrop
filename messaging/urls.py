from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("conversation_list/", views.conversation_list, name="conversation_list"),
    path("<int:conversation_id>/", views.conversation_detail, name="conversation_detail"),
    path("<int:conversation_id>/send/", views.send_message, name="send_message"),
    path("start/<int:user_id>/", views.start_conversation, name="start_conversation"),
]

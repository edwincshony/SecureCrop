from django.urls import path
from . import views

app_name = "discussions"

urlpatterns = [
    path('category_list/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.thread_list, name='thread_list'),
    path('category/<int:category_id>/create-thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/create-post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/reply/', views.reply_to_post, name='reply_to_post'),
    path('add-category/', views.add_category, name='add_category'),
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:post_id>/downvote/', views.downvote_post, name='downvote_post'),
]
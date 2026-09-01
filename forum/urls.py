from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/create/', views.thread_create, name='thread_create'), 
    path('thread/<int:thread_id>/view/', views.increment_views, name='increment_views'), 
    path('thread/<int:thread_id>/delete/', views.delete_thread, name='delete_thread'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
]

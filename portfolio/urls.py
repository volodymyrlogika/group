from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    CustomLoginView,
    RegisterView,
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    
    # Авторизація
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
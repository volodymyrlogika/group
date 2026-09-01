from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, ProjectImage
from .forms import ProjectForm, RegisterForm, LoginForm


# --- АВТОРИЗАЦІЯ ТА РЕЄСТРАЦІЯ ---
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'portfolio/login.html'
    redirect_authenticated_user = True


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'portfolio/register.html'
    success_url = reverse_lazy('login')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('project_list')


# --- СПИСОК ПРОЄКТІВ ---
class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    ordering = ['-id']


# --- ДЕТАЛІ ПРОЄКТУ ---
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'


# --- СТВОРЕННЯ ПРОЄКТУ ---
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        images = self.request.FILES.getlist('images')
        for img in images:
            ProjectImage.objects.create(project=self.object, image=img)

        return response


# --- РЕДАГУВАННЯ ПРОЄКТУ ---
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        images = self.request.FILES.getlist('images')
        for img in images:
            ProjectImage.objects.create(project=self.object, image=img)

        delete_image_ids = self.request.POST.getlist('delete_images')
        if delete_image_ids:
            ProjectImage.objects.filter(id__in=delete_image_ids, project=self.object).delete()

        return response


# --- ВИДАЛЕННЯ ПРОЄКТУ ---
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'portfolio/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
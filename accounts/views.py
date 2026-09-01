from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from accounts.forms import LoginForm, RegisterForm

from django.views.generic import TemplateView
from forum.models import Thread
from systemreq.models import Servey

from django.contrib.auth import logout


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
       
        context["latest_threads"] = Thread.objects.order_by('-created_at')[:3]
        context["latest_surveys"] = Servey.objects.order_by('-date_created')[:3]
        
        return context


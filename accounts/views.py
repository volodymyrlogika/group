from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from accounts.forms import LoginForm, RegisterForm

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

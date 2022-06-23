from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.views.generic import CreateView
from datetime import datetime


class HomeView(TemplateView):
    template_name = 'welcome.html'
    extra_context = {'today': datetime.today()}


class LoginInterfaceView(LoginView):
    template_name = 'login.html'


class LogoutInterfaceView(LogoutView):
    template_name = 'logout.html'


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = 'login'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('stocks.portfolio')
        return super().get(request, *args, **kwargs)

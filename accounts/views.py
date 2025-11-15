from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import LoginForm

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')  # Redirect to our home page after login

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Logged in successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid credentials.')
        return super().form_invalid(form)

def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('login')

# Placeholder home view (requires login, redirects to login if unauthorized)
# Later, this can redirect to products app
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'  # To be created later, aligned with project (e.g., welcome for admins)

    def handle_no_permission(self):
        messages.warning(self.request, 'No permission to access this page.')
        return redirect('login')
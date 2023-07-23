from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DetailView, CreateView, FormView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from django.urls import reverse_lazy


class LoginView(LoginView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class LogoutView(LogoutView):
    next_page = reverse_lazy('login')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class UserPageView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user/user_page.html'
    context_object_name = 'user_page'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_login_url(self):
        return reverse_lazy('login')


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = 'user/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Your password has been successfully changed.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

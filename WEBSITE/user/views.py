from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            return HttpResponseRedirect('/')

        return render(request, 'user/login.html', {'form': form})

    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'user/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'user/register.html', {'form': form})


class UserPageView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }
        return render(request, 'user/user_page.html', context)


class ChangePasswordView(View):
    template_name = 'user/change_password.html'
    form_class = PasswordChangeForm
    success_url = '/'

    @login_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully changed.')
            return redirect(self.success_url)
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, self.template_name, {'form': form})

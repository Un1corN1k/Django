from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('change_password/', change_password, name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout_view'),
    path('change-password/', change_password, name='change_password'),
    path('user_page/', user_page, name="user_page")
]
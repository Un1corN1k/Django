from django.urls import path

from .views import (
    ChangePasswordView,
    LoginView,
    RegisterView,
    LogoutView,
    UserPageView,
)

urlpatterns = [
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('user_page/', UserPageView.as_view(), name='user_page'),
]

from django.urls import path
from .views import base_template, first

urlpatterns = [
    path('', base_template),
    path('first/', first),
]
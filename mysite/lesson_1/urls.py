from django.urls import path
from .views import index

urlpatterns = [
    path('api/v1/index/<str:name>/', index, name="index"),
]


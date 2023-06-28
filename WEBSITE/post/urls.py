from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('add_comment/<slug:slug>/', add_comment, name='add_comment'),
    path('create/', create_post, name='create_post'),
    path('delete_post/<slug:slug>/', delete_post, name='delete_post'),
    path('view_post/<slug:slug>/', view_post, name='view_post'),
]
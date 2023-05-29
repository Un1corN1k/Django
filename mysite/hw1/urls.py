from django.urls import path
from .views import *

urlpatterns = [
    path('blogs/', home, name='home'),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('<slug>/', blog, name='blog'),
    path('<slug>/comment/', add_comment, name='add_comment'),
    path('create/', create_post, name='create_post'),
    path('<slug>/update/', update_post, name='update_post'),
    path('<slug>/delete/', delete_post, name='delete_post'),
    path('profile/<username>/', profile, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]


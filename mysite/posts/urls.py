from django.urls import path
from .views import all_posts, post_detail

urlpatterns = [
    path('', all_posts, name="all_posts"),
    path('<int:post_id>/', post_detail, name="post_detail"),
]
from django.urls import path
from .views import (
    HomeView,
    AddCommentView,
    CreatePostView,
    DeletePostView,
    ViewPostView,
    CreateTopicView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add_comment/<slug:slug>/', AddCommentView.as_view(), name='add_comment'),
    path('create/', CreatePostView.as_view(), name='create_post'),
    path('delete_post/<slug:slug>/', DeletePostView.as_view(), name='delete_post'),
    path('view_post/<slug:slug>/', ViewPostView.as_view(), name='view_post'),
    path('create_topic/', CreateTopicView.as_view(), name='create_topic'),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hw1.urls')),
    path('', include("lesson_1.urls")),
    path('template/', include("lesson_2.urls")),
    path('posts/', include("posts.urls")),
]

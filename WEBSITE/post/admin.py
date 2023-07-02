from django.contrib import admin
from .models import Topic, BlogPost, Comment


@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "created_at"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", 'description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "created_at"]

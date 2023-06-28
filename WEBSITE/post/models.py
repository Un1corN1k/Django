from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class BlogPost(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=120, default="enter your title")
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, blank=True, null=True)
    content = models.TextField(max_length=5000, default="enter your description")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.id:
            self.slug = slugify(self.title)
            if not self.topic:
                available_topics = Topic.objects.all()
                if available_topics.exists():
                    self.topic = available_topics.first()
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return str(self.title)


class Topic(models.Model):
    topic = models.CharField(max_length=100, default="enter your topic")
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics", blank=True, null=True)

    def __str__(self):
        return str(self.topic)


class Comment(models.Model):
    content = models.CharField(max_length=120)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.content)

from django.db import models
from slugify import slugify
from django.contrib.auth.models import User


class BlogPost(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length= 120, default= "without a hw topic")
    comment = models.ManyToManyField("Comment", blank=True)
    topic = models.ManyToManyField("Topic", blank=True)
    content = models.TextField(max_length= 5000, default= "empty")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return str(self.title)


class Topic(models.Model):
    title = models.CharField(max_length= 120)
    description = models.CharField(max_length= 120)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topics", blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    content = models.CharField(max_length= 120)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)

    def __str__(self):
        return str(self.content)

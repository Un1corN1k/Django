from django import forms
from .models import BlogPost, Comment, Topic


class PostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content"]


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]


class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description"]

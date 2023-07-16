from django import forms

from .models import BlogPost, Comment, Topic
from django.contrib.auth.models import User


class PostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", 'topic', "content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["id", 'topic', "description"]


class FilterForm(forms.Form):
    authors = forms.ModelChoiceField(
        queryset=User.objects.filter(id__in=BlogPost.objects.values_list('author_id', flat=True).distinct()),
        empty_label="All Authors",
        required=False)

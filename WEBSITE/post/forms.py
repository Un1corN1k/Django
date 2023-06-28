from django import forms
from .models import BlogPost, Comment, Topic


class PostModelForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title",'topic', "content"]
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
        fields = ['topic', "description"]

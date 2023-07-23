from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, FormView, DeleteView
from .forms import PostModelForm, CommentModelForm, TopicModelForm, FilterForm
from .models import BlogPost, Topic
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = BlogPost
    template_name = 'post/home.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FilterForm(self.request.GET)

        if form.is_valid():
            author_filter = form.cleaned_data['authors']

            if author_filter:
                queryset = queryset.filter(author=author_filter)

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        return context


class ViewPostView(DetailView):
    model = BlogPost
    template_name = 'post/view_post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'


class AddCommentView(FormView):
    template_name = 'post/add_comment.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        slug = self.kwargs['slug']
        blog = get_object_or_404(BlogPost, slug=slug)
        comment = form.save(commit=False)
        comment.blog = blog
        comment.author = self.request.user
        comment.save()
        return redirect('view_post', slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        blog = get_object_or_404(BlogPost, slug=slug)
        context['blog'] = blog
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = PostModelForm
    template_name = 'post/create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'post/delete_post.html'
    success_url = reverse_lazy('post/home')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if self.request.user != obj.author:
            raise PermissionDenied
        return obj


class CreateTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicModelForm
    template_name = 'post/create_topic.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

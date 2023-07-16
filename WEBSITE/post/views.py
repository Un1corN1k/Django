
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .forms import PostModelForm, CommentModelForm, TopicModelForm, FilterForm
from .models import BlogPost
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def get(self, request):
        form = FilterForm(request.GET)
        blogs = BlogPost.objects.all()

        if form.is_valid():
            author_filter = form.cleaned_data['authors']

            if author_filter:
                blogs = blogs.filter(author=author_filter)

        search_query = request.GET.get('search')
        if search_query:
            blogs = blogs.filter(title__icontains=search_query)

        context = {
            'blogs': blogs,
            'form': form,
        }
        return render(request, 'post/home.html', context)


class ViewPostView(View):
    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug)
        context = {'post': post}
        return render(request, 'post/view_post.html', context)


class AddCommentView(View):
    @method_decorator(login_required(login_url='user/login'))
    def get(self, request, slug):
        blog = get_object_or_404(BlogPost, slug=slug)
        form = CommentModelForm()
        context = {
            'blog': blog,
            'form': form
        }
        return render(request, 'post/add_comment.html', context)

    @method_decorator(login_required(login_url='user/login'))
    def post(self, request, slug):
        blog = get_object_or_404(BlogPost, slug=slug)
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('view_post', slug=slug)

        context = {
            'blog': blog,
            'form': form
        }
        return render(request, 'post/add_comment.html', context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = PostModelForm
    template_name = 'post/create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, slug):
        blog = get_object_or_404(BlogPost, slug=slug)

        if request.user == blog.author:
            blog.delete()
            return redirect("/")

        return redirect('post/home')

    def get(self, request, slug):
        blog = get_object_or_404(BlogPost, slug=slug)

        if request.user == blog.author:
            return render(request, 'post/delete_post.html', {'blog': blog})

        return redirect('post/home')


class CreateTopicView(LoginRequiredMixin, View):
    def post(self, request):
        form = TopicModelForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('/')

        return render(request, 'post/create_topic.html', {'form': form})

    def get(self, request):
        form = TopicModelForm()
        return render(request, 'post/create_topic.html', {'form': form})
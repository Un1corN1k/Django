from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostModelForm, CommentModelForm
from .models import BlogPost
from django.contrib.auth.decorators import login_required


def home(request):
    blogs = BlogPost.objects.all()

    topic_filter = request.GET.get('topic')
    if topic_filter:
        blogs = blogs.filter(topic=topic_filter)

    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(title__icontains=search_query)

    return render(request, 'post/home.html', {'blogs': blogs})


def view_post(request, slug):
    post = get_object_or_404(BlogPost, slug= slug)
    return render(request, 'post/view_post.html', {'post': post})


def add_comment(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('view_post', slug=slug)
    else:
        form = CommentModelForm()

    context = {
        'blog': blog,
        'form': form
    }
    return render(request, 'post/add_comment.html', context)


def create_post(request):
    if not request.user.is_authenticated:
        return redirect('post/login')

    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
    form = PostModelForm()
    return render(request, 'post/create_post.html', {'form': form})


@login_required
def delete_post(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)

    if request.user == blog.author:
        if request.method == 'POST':
            blog.delete()
            return redirect("/")

        return render(request, 'post/delete_post.html', {'blog': blog})
    else:
        return redirect('post/home')


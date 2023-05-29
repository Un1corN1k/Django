from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def blog(request, slug):
    return render(request, 'blog.html', {'slug': slug})


def add_comment(request, slug):
    return HttpResponse("Додавання коментаря до посту '{}'".format(slug))


def create_post(request):
    return render(request, 'create_post.html')


def update_post(request, slug):
    return HttpResponse("Оновлення поста '{}'".format(slug))


def delete_post(request, slug):
    return HttpResponse("Видалення поста '{}'".format(slug))


def profile(request, username):
    return render(request, 'profile.html', {'username': username})


def change_password(request):
    return render(request, 'change_password.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'logout.html')

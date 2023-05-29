from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest, name):
    return HttpResponse(f"Hello world, {name}")

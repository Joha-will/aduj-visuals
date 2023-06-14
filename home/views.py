from django.shortcuts import render


def index(request):
    """A view render's the home page"""
    return render(request, "home/index.html")

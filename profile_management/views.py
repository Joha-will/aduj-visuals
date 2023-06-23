from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages


@login_required
def view_profile(request):
    """A view that renders the user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)
    template = 'profile_management/view_profile.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

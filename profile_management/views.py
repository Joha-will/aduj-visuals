from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages
from .forms import UserProfileForm
from checkout.models import Order


@login_required
def view_profile(request):
    """A view that renders the user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated successfully')
            return redirect(reverse('view_profile',))

        else:
            messages.error(request, 'Unable to update profile,\
                        please check form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    template = 'profile_management/view_profile.html'
    context = {
        'form': form,
        'orders': orders,
    }
    return render(request, template, context)

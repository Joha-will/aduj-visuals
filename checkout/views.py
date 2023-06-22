from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from .forms import OrderForm


def checkout(request):

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, " There's nothing in your basket!")
        return redirect(reverse('products'))

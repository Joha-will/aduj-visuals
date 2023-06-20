from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_basket(request):
    """ A view that renders the products in the basket """
    return render(request, "basket/view_basket.html")
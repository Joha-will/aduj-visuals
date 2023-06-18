from django.shortcuts import render, get_object_or_404
from . models import Product


def all_products(request):
    """ A view that displays all product to customers"""
    products = Product.objects.all()

    context = {
        'products': products,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """ A view that displays products individually"""
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }
    return render(request, "products/product_detail.html", context)

from django.shortcuts import render, reverse, redirect, get_object_or_404
from .forms import ProductForm
from products.models import Product, Category
from django.contrib import messages


def add_product(request):
    """ Add's products to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.info(request, 'Product added successfully!')
            return redirect(reverse('products'))
        else:
            messages.error(request, 'Unable to add product.\
                            Please check form is valid.')
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'store_management/add_product.html', context)


def edit_product(request, product_id):
    """ Edit product's in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Product updated successfully.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Unable to update product.\
                            Please check form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing this product\
             ({ product.name })')
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'store_management/edit_product.html', context)